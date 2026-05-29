# System Architecture & Storage System

This document provides a high-level view of the decoupled architecture, data schema representation, and caching mechanism used in the Antigravity Headless CMS Engine.

---

## 🏛️ High-Level Design

The engine leverages a completely **decoupled/headless design**, enforcing a strict boundary between storage, schema creation, content compilation, and consumer APIs.

```
       +---------------------------------------------+
       |           The Content Studio (React)        |
       |  - Drag & Drop Schema Builder               |
       |  - Dynamic Content Writer (Draft/Published) |
       |  - Media Assets Manager                     |
       +---------------------------------------------+
                              |
                              | HTTPS / JSON
                              v
       +---------------------------------------------+
       |         FastAPI Omnichannel Gateway         |
       |  - JWT Authentication Middleware             |
       |  - Schema Validation Compiler               |
       |  - Media Upload & Optimization (Pillow WebP)|
       +---------------------------------------------+
               |                             |
               | (SQLAlchemy ORM)            | (Cache read/write)
               v                             v
       +--------------------+        +---------------+
       | PostgreSQL / SQLite|        | Redis Cache   |
       | Primary Data Store |        | (API Layer)   |
       +--------------------+        +---------------+
```

---

## 💾 Primary Data Storage Model

To maintain modularity and high performance while allowing schema alterations on the fly, the database uses a hybrid design representing Collections and Fields in structured metadata tables, while the content data is represented within a JSON/JSONB field.

### 1. Platform-Independent GUID & JSON Implementation
To allow effortless local development without complex database configuration, the SQLAlchemy configuration implements a platform-independent `GUID` type decorator and relies on standard `JSON` column serialization. 

- **PostgreSQL Context**: The models automatically compile down to the native optimized `UUID` and `JSONB` data columns.
- **SQLite Context**: Maps to `CHAR(36)` columns for IDs and serialized string columns for JSON, allowing rapid development using local `.db` files without sacrificing the ability to run on production-ready environments.

---

## 🗄️ Database Schemas

### 1. `users`
Tracks CMS administrators and editors, managing permissions via simple role checks.
- `id` (GUID/UUID, PK)
- `email` (String, unique, index)
- `hashed_password` (String)
- `role` (String: `Admin` | `Editor`)
- `created_at` (DateTime)

### 2. `collections`
Registers user-defined collection entities (e.g. "Products", "Blog Posts").
- `id` (GUID/UUID, PK)
- `name` (String, unique)
- `slug` (String, unique, index)
- `description` (Text)
- `created_at` (DateTime)

### 3. `fields`
Maintains structural schemas linked to collections. Contains custom validations like lengths or value bounds.
- `id` (GUID/UUID, PK)
- `collection_id` (GUID/UUID, FK -> `collections.id`)
- `name` (String)
- `field_type` (String: `Text` | `Number` | `Boolean` | `RichText` | `Image`)
- `is_required` (Boolean)
- `validations` (JSON, dictionary format)
- `created_at` (DateTime)

### 4. `contents`
Houses dynamic JSON content records matching the parsed collection structure.
- `id` (GUID/UUID, PK)
- `collection_id` (GUID/UUID, FK -> `collections.id`)
- `data` (JSON, containing dynamic records)
- `status` (String: `Draft` | `Published`)
- `created_by` (GUID/UUID, FK -> `users.id`)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### 5. `audit_logs`
Records historical snapshots of the data prior to updates. Used to track changes, user edits, and support content recovery rollbacks.
- `id` (GUID/UUID, PK)
- `content_id` (GUID/UUID, FK -> `contents.id`)
- `previous_data` (JSON)
- `changed_by` (GUID/UUID, FK -> `users.id`)
- `changed_at` (DateTime)

### 6. `media`
Stores uploaded binary metadata assets optimized to WebP structures.
- `id` (GUID/UUID, PK)
- `filename` (String)
- `url` (String)
- `mime_type` (String)
- `size_bytes` (BigInteger)
- `uploaded_by` (GUID/UUID, FK -> `users.id`)
- `created_at` (DateTime)

---

## ⚡ Redis API Caching Strategy

The omnichannel gateway can be layered with Redis to optimize public API throughput:
- **Keyspace format**: `cms:cache:collection:{slug}`
- **Cache Invalidation**: Every time an editor issues a POST, PUT, or DELETE request altering content within a specific collection, the corresponding Redis keys are invalidated to ensure consumers retrieve real-time data while preserving fast load times for static/read requests.
