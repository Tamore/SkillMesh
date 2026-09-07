# SkillMesh 🌐
### A High-Fidelity Talent Discovery & Collaboration Mesh

<div align="center">
  <img src="docs/logo_official.png" alt="SkillMesh Official Logo" width="800">
</div>


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20059940.svg)](https://doi.org/10.5281/zenodo.20059940)

**SkillMesh** is a high-performance talent discovery mesh and distributed observability framework.
- **Published Paper (v1):** [DOI 10.5281/zenodo.20059940](https://doi.org/10.5281/zenodo.20059940) (*SkillMesh: Analyzing Event-Driven Workflows in a Centralized Application Environment*)


---

## 🏛️ System Architecture & Distributed Flow

````mermaid
graph TD
    subgraph CLIENT[CLIENT & OBSERVABILITY LAYER]
        WebHUD[SkillMesh Web Dashboard / 3D Topology HUD]
        Tracer[OpenTelemetry / Jaeger Distributed Tracer]
    end

    subgraph BUS[MESSAGING & EVENT BUS LAYER]
        RedisBus[Redis Streams Event Bus]
    end

    subgraph WORKERS[DISTRIBUTED WORKER NODES]
        Coord[Coordinator Node<br/>Dispatcher & OTel Injector]
        WorkerA[Worker Alpha<br/>Inference Simulator]
        WorkerB[Worker Beta<br/>State Storage]
    end

    Coord -->|1. Publish Task + TraceID| RedisBus
    RedisBus -->|2. Consume & Process| WorkerA
    WorkerB -->|3. Heartbeat Pings| RedisBus

    RedisBus -->|4. Real-time Stream| WebHUD
    RedisBus -->|5. Trace Aggregation| Tracer
`---

## 🚀 Evolution to SkillMesh v2: Distributed Systems Architecture

SkillMesh has evolved from a single-node application into a **Distributed Event-Driven Observability Framework** designed to benchmark microsecond multi-agent telemetry and fault-tolerant coordination:

### 1. 🐳 Multi-Container Microservice Architecture
- **Worker Swarm Decoupling:** Instead of running all execution within a single monolith, SkillMesh v2 decouples workloads across containerized microservices:
  - **Coordinator Node (services/coordinator):** Manages task scheduling, W3C trace context generation, and API dispatching.
  - **Inference Worker (Worker-Alpha):** Isolated container worker processing task workloads asynchronously.
  - **State Memory Worker (Worker-Beta):** Dedicated worker managing state persistence and memory streams.

### 2. 📡 Redis Streams Asynchronous Event Bus
- **Decoupled Messaging:** Replaced synchronous internal queues with a high-throughput **Redis Streams** event bus (skillmesh:events), enabling non-blocking pub/sub communication between microservices.

### 3. ⏱️ OpenTelemetry Microsecond Tracing
- **W3C Context Propagation:** Injects OpenTelemetry TraceID and SpanID directly into Redis event headers.
- **Per-Hop Latency Measurement:** As tasks move across containers, workers extract trace context and log precise microsecond traversal latency to OpenTelemetry / Jaeger.

### 4. 💓 Self-Healing Heartbeat & Fault Tolerance
- **Automated Node Health Monitoring:** Worker nodes emit periodic heartbeat frames every 2 seconds to skillmesh:heartbeats.
- **Node Crash Detection:** If a container fails to ping within 4 seconds, the Coordinator flags the node as UNHEALTHY and automatically re-queues unacknowledged tasks.


---

**SkillMesh** is a professional-grade talent discovery platform built for the modern technical workforce. It moves beyond standard social networking by focusing on **Skills as the Primary Asset**, using a high-fidelity "Stitch-inspired" UI to facilitate seamless connections between innovators, engineers, and founders.

---

## ✨ Core Features

- **🚀 Instant Identity**: One-click social authentication via Google and GitHub.
- **🔍 Talent Mesh**: Global search for experts based on specific technical skill sets.
- **📡 Broadcast Signaling**: A centralized feed for "Hiring," "Open to Work," and general technical updates.
- **📊 System Insights & Analytics**: A dedicated Founder dashboard for tracking event-driven protocol statistics and exporting research data.
- **💬 Secure Handshakes**: Integrated peer-to-peer messaging for direct collaboration.
- **⚡ Precision UX**: Real-time interaction feedback, including global loading states and interactive button protocols.
- **💎 Editorial Aesthetic**: A custom-built dark-mode design system utilizing Glassmorphism and premium typography.

---

## 🛠️ The Technical Stack

SkillMesh is built with a robust, event-driven architecture designed for scalability and performance.

### **The Backend Engine & Microservices (v1 + v2)**
- **Django (Python)**: Core framework for web business logic and Vercel serverless deployment.
- **FastAPI (Python)**: High-performance microservice Coordinator node handling asynchronous task dispatching.
- **Redis Streams**: Decoupled event bus (skillmesh:events) for inter-service message passing.
- **OpenTelemetry SDK**: W3C TraceContext context propagation injecting microsecond TraceID & SpanID across container hops.
- **Supabase (PostgreSQL)**: Distributed cloud database for high-availability data persistence.
- **Docker & Docker Compose**: Containerized multi-node cluster orchestration for worker node swarms.
- **django-allauth & PyJWT**: Secure authentication and identity verification.

### **The Frontend (Stitch-Inspired)**
- **Tailwind CSS**: A utility-first CSS framework for custom premium components.
- **Glassmorphism**: Advanced UI techniques (backdrop filters, opacity layering) for a "Neon Tokyo" look.
- **Modern Typography**: Inter and Sora font families from Google Fonts.
- **Interactive JS**: Custom vanilla JavaScript for real-time UI state management.

---

## 🧪 Research Context: Event-Driven System Design

SkillMesh is not just a social platform—it is designed as an **experimental system for studying event-driven architectures in digital ecosystems**.

### 🔄 Event-Driven Design
All major user interactions are treated as system events, including:
- `UserRegistered` • `ProfileUpdated` • `SkillAdded` • `PostCreated` • `MessageSent`

Each event is **Logged**, **Timestamped**, **Measured for Latency**, and **Validated for Status**. This provides a granular audit trail for analyzing system behavior under load.

### 📊 Reliability Evaluation
SkillMesh includes an internal event tracking mechanism that enables:
- **Latency Measurement**: Tracking event processing speed in milliseconds.
- **Protocol Health**: Monitoring system success/failure rates.
- **Workflow Analysis**: Studying execution behavior across distributed components.

### 🎯 Research Alignment
The platform serves as a **prototype for studying how real-world applications behave under event-driven models**, bridging the gap between theoretical system design and practical implementation in the fields of Distributed Systems and Software Engineering.

---

## ⚙️ Installation & Setup

To initialize your own local SkillMesh instance, follow these protocol steps:

### 1. Clone the Protocol
```bash
git clone https://github.com/SkillMesh/skillmesh.git
cd skillmesh
```

### 2. Environment Configuration
Create a `.env` file in the root directory and populate it with your cloud credentials:
```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@db.supabase.co:5432/postgres
```

### 3. Dependency Initialization
```bash
pip install -r requirements.txt
```

### 4. Database Migration
```bash
python manage.py migrate
python manage.py seed_data  # Populates the mesh with initial test talent
```

### 5. Launch the Mesh
```bash
python manage.py runserver
```

---