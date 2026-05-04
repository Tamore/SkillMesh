# SkillMesh 🌐
### A High-Fidelity Talent Discovery & Collaboration Mesh

<div align="center">
  <img src="docs/logo_official.png" alt="SkillMesh Official Logo" width="800">
</div>

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

### **The Backend Engine**
- **Django (Python)**: The core framework for business logic and data orchestration.
- **Supabase (PostgreSQL)**: Distributed cloud database for high-availability data persistence.
- **django-allauth**: Enterprise-grade authentication handling OAuth2 handshakes.
- **Cryptography & PyJWT**: Secure token-based identity verification.

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

## 📐 Architecture Overview

SkillMesh follows a **Service Layer Pattern**, separating complex business logic from the UI views. This ensures the code is:
- **Testable**: Logic is decoupled from HTTP requests.
- **Maintainable**: Clear separation of concerns between database, logic, and presentation.
- **Event-Aware**: The system tracks interaction events (like search queries and post updates) for analytical insights.

---

## 🎨 Design Philosophy

The SkillMesh aesthetic is heavily inspired by the **Stitch design system**, focusing on:
- **High Contrast**: Deep grays (`#000000` to `#111111`) paired with vibrant neon accents.
- **Frictionless UI**: Minimizing clicks via one-click logins and auto-profile generation.
- **Editorial Layouts**: Using premium typography and generous spacing to make technical information scannable and beautiful.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Created with passion for the technical community.*
