import os
import time
import json
import threading
import redis
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

node_id = os.getenv('NODE_ID', 'Worker-Unknown')
node_role = os.getenv('NODE_ROLE', 'Generic-Worker')

# Initialize OpenTelemetry
otlp_endpoint = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4318')
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=f'{otlp_endpoint}/v1/traces'))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# Redis Connection
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))

def get_redis():
    return redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

def emit_heartbeats():
    while True:
        try:
            r = get_redis()
            hb_data = {
                'node_id': node_id,
                'role': node_role,
                'timestamp': time.time()
            }
            r.hset('skillmesh:heartbeats', node_id, json.dumps(hb_data))
        except Exception as e:
            pass
        time.sleep(2.0)

def consume_events():
    stream_key = 'skillmesh:events'
    group_name = 'skillmesh-workers'
    consumer_name = node_id

    while True:
        try:
            r = get_redis()
            try:
                r.xgroup_create(stream_key, group_name, id='0', mkstream=True)
            except Exception:
                pass

            print(f'[{node_id}] Listening for tasks on stream {stream_key}...')
            while True:
                entries = r.xreadgroup(group_name, consumer_name, {stream_key: '>'}, count=1, block=2000)
                if not entries:
                    continue

                for stream, messages in entries:
                    for msg_id, message in messages:
                        target_role = message.get('target_role')
                        if target_role and target_role != node_role:
                            continue

                        carrier = json.loads(message.get('carrier', '{}'))
                        parent_context = TraceContextTextMapPropagator().extract(carrier)

                        with tracer.start_as_current_span(f'worker_process_{node_role}', context=parent_context) as span:
                            dispatched_at = int(message.get('dispatched_at_us', 0))
                            now_us = time.time_ns() // 1000
                            latency_us = now_us - dispatched_at if dispatched_at > 0 else 0

                            span.set_attribute('node_id', node_id)
                            span.set_attribute('node_role', node_role)
                            span.set_attribute('hop_latency_us', latency_us)
                            task_id = message.get('task_id', 'N/A')
                            span.set_attribute('task_id', task_id)

                            time.sleep(0.015)
                            print(f'[{node_id}] Processed Task {task_id} | Hop Latency: {latency_us / 1000:.2f}ms')
                            r.xack(stream_key, group_name, msg_id)

        except Exception as e:
            time.sleep(2.0)

if __name__ == '__main__':
    threading.Thread(target=emit_heartbeats, daemon=True).start()
    consume_events()
