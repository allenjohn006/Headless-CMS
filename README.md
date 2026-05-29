# Antigravity Headless CMS Engine 🚀

An enterprise-grade, highly performant, production-ready Headless CMS Engine built from scratch. This decoupled architecture allows non-technical content creators to define schema architectures and compile dynamic content on-the-fly, while developers consume robust, cached APIs.

Developed as a monorepo featuring a **Python (FastAPI) Backend** and a premium **React (Vite + TypeScript) Dashboard**.

---

## 🏗️ Architecture & Core Components

```
cms-engine/
├── backend/                  # FastAPI Web Server
│   ├── app/
│   │   ├── api/              # API Route Handlers (v1)
│   │   │   ├── auth.py       # JWT & Role-Based Access Control
│   │   │   ├── collections.py# Custom Collection & Field Builders
│   │   │   ├── content.py    # Dynamic Content CRUD & Query Gateway
│   │   │   └── media.py      # Image uploads & optimized WebP variants
│   │   ├── core/             # Base configurations & security
│   │   ├── db/               # SQLAlchemy Session & Models (SQLite/Postgres)
│   │   ├── schemas/          # Pydantic Schemas & Types
│   │   └── services/         # Schema validation, optimization, and auditing
│   └── requirements.txt
├── docs/                     # Technical Documentation
│   ├── architecture.md       # High-level architecture and storage
│   ├── api_endpoints.md      # API Reference and interactive usage
│   └── schema_compiler.md    # Schema Compiler validation engine
├── frontend/                 # The Content Studio Dashboard (React + TypeScript)
│   ├── src/
│   │   ├── components/       # Custom modular components
│   │   └── App.tsx           # Layout, routing, and UI views
│   └── package.json
└── docker-compose.yml        # PostgreSQL & Redis dockerization
```

---

## ⚡ Features

### 💻 1. Dynamic Content Architect (The Engine)
- Define **Collections** (e.g. `Blog Posts`, `Products`) and attach dynamic **Fields** (`Text`, `Number`, `Boolean`, etc.) on the fly.
- Optimized hybrid database models supporting platform-independent `GUID` and `JSON` type serialization across PostgreSQL (using `JSONB`) and SQLite.
- Seamless **Draft vs. Published** state validation for every content entry.

### 🛡️ 2. Role-Based Access Control & Versioning
- Secure JWT-based Authentication with strict **Admin** vs. **Editor** role enforcement.
- **Audit Logging System**: Keeps a snapshot of the prior state in `audit_logs` every time a dynamic content is edited, enabling full version history.

### 🌐 3. Omnichannel API Gateway (The Delivery)
- Fully dynamic, parameterized endpoints (`/api/v1/content/{collection_slug}`) supporting sorting (`?sort=-created_at`), limit/offset pagination, and draft filtering.
- Fully auto-generated **OpenAPI/Swagger** documentation for absolute developers' integration.

### 🖼️ 4. Image Upload & Optimization
- Intercepts raw images, dynamically resizes large images (max 1200px width), and converts them on-the-fly to ultra-compact **WebP** formats upon upload to preserve storage and bandwith.

### 🎨 5. The Content Studio (The Interface)
- A modern, high-fidelity dark-mode interface built using Vite + React + TypeScript.
- Clean navigation sidebar, fully customized analytics dashboard, dynamic schema builder, and content preview interface.

---

## 🚀 Quick Start (Local Run)

The codebase has been refactored to support **SQLite Fallback** out-of-the-box, meaning you do not need Docker running to start developing!

### 🟢 Running the Backend
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Install the python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI development server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   *The backend will boot up at **[http://127.0.0.1:8000](http://127.0.0.1:8000)** and automatically seed your testing accounts!*

### 🔵 Running the Frontend Content Studio
1. Navigate to the frontend folder:
   ```bash
   cd ../frontend
   ```
2. Install standard Node packages:
   ```bash
   npm install
   ```
3. Boot up Vite React dev server:
   ```bash
   npm run dev
   ```
   *The client interface will run at **[http://localhost:5173/](http://localhost:5173/)**.*

---

## 👥 Default Seeded Credentials

When running the backend, it will automatically populate your databases with two distinct RBAC accounts:

| Role | Email | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@example.com` | `adminpass` | Create collections, fields, and manage engine settings |
| **Editor** | `editor@example.com` | `editorpass` | Manage, publish, edit, and audit content entries |

---

## 📚 Deep-Dive Documentation

For more exhaustive explanations, check out the documentation files inside the `docs/` folder:
- 📖 [System Architecture & DB Storage](docs/architecture.md)
- 📖 [Omnichannel API Reference Guide](docs/api_endpoints.md)
- 📖 [Schema Compiler & Dynamic Validation Engine](docs/schema_compiler.md)
