import os
import time
import json
import uuid
import redis
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

# Initialize OpenTelemetry
otlp_endpoint = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://jaeger-tracer:4318')
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=f'{otlp_endpoint}/v1/traces'))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = FastAPI(title='SkillMesh v2 Coordinator Node')

# Redis Connection
redis_host = os.getenv('REDIS_HOST', 'redis-bus')
redis_port = int(os.getenv('REDIS_PORT', 6379))
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

class TaskRequest(BaseModel):
    target_role: str = 'Inference-Simulator'
    payload: dict = {'action': 'BENCHMARK_TEST', 'data_size_kb': 64}

@app.get('/')
def health_check():
    return {'status': 'ONLINE', 'node': os.getenv('NODE_NAME', 'Coordinator-Main')}

@app.post('/dispatch')
def dispatch_task(request: TaskRequest):
    with tracer.start_as_current_span('coordinator_dispatch_task') as span:
        trace_id = format(span.get_span_context().trace_id, '032x')
        span_id = format(span.get_span_context().span_id, '016x')
        
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        
        task_id = str(uuid.uuid4())
        event_payload = {
            'task_id': task_id,
            'trace_id': trace_id,
            'span_id': span_id,
            'carrier': json.dumps(carrier),
            'target_role': request.target_role,
            'payload': json.dumps(request.payload),
            'dispatched_at_us': time.time_ns() // 1000
        }
        
        # Publish to Redis Stream
        stream_key = 'skillmesh:events'
        r.xadd(stream_key, event_payload)
        
        span.set_attribute('task_id', task_id)
        span.set_attribute('target_role', request.target_role)
        
        return {
            'status': 'DISPATCHED',
            'task_id': task_id,
            'trace_id': trace_id,
            'stream': stream_key
        }

@app.get('/cluster-status')
def get_cluster_status():
    heartbeats = r.hgetall('skillmesh:heartbeats')
    active_nodes = {}
    current_time = time.time()
    
    for node_id, data_str in heartbeats.items():
        try:
            data = json.loads(data_str)
            last_ping = data.get('timestamp', 0)
            is_healthy = (current_time - last_ping) < 6.0
            active_nodes[node_id] = {
                'role': data.get('role'),
                'status': 'HEALTHY' if is_healthy else 'UNHEALTHY',
                'seconds_since_ping': round(current_time - last_ping, 2)
            }
        except Exception:
            pass
            
    return {'active_nodes': active_nodes, 'total_registered': len(active_nodes)}
