# API Reference & Endpoints Guide

The Antigravity Headless CMS Engine exposes modular, high-performance API endpoints. This guide details standard requests, parameters, role requirements, and expected structures.

---

## 🔒 Authentication Layer

All endpoints require JWT authorization headers (except for content retrieval which is public, but can optionally be restricted via middleware).

```http
Authorization: Bearer <your_jwt_access_token>
```

### 1. Register User
- **Endpoint**: `POST /api/v1/auth/register`
- **Access**: Public
- **Payload**:
  ```json
  {
    "email": "user@example.com",
    "password": "strongpassword123",
    "role": "Editor"
  }
  ```
- **Response**: `200 OK`

### 2. Login
- **Endpoint**: `POST /api/v1/auth/login`
- **Access**: Public (requires standard OAuth2 form inputs)
- **Payload** (Form-Data):
  - `username`: `user@example.com`
  - `password`: `strongpassword123`
- **Response**:
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer"
  }
  ```

---

## 📂 Collections Management

### 1. Create a Collection
- **Endpoint**: `POST /api/v1/collections/`
- **Access**: Admin Only
- **Payload**:
  ```json
  {
    "name": "Blog Posts",
    "slug": "posts",
    "description": "Dynamic collection for company news and posts."
  }
  ```
- **Response**: `200 OK` containing created Collection uuid and timestamp metadata.

### 2. Create Dynamic Fields
- **Endpoint**: `POST /api/v1/collections/{collection_id}/fields`
- **Access**: Admin Only
- **Payload**:
  ```json
  {
    "name": "title",
    "field_type": "Text",
    "is_required": true,
    "validations": {
      "min_length": 5,
      "max_length": 150
    }
  }
  ```

---

## ✍️ Dynamic Content CRUD (The Engine)

### 1. Create Content Entry
- **Endpoint**: `POST /api/v1/content/{collection_slug}`
- **Access**: Admin or Editor
- **Payload**:
  ```json
  {
    "data": {
      "title": "Welcome to the Headless CMS",
      "author": "Senior Principal Engineer"
    },
    "status": "Published"
  }
  ```
- **Response**: `201 Created`

### 2. Update Content (Creates Audit Log)
- **Endpoint**: `PUT /api/v1/content/{collection_slug}/{content_id}`
- **Access**: Admin or Editor
- **Payload**:
  ```json
  {
    "data": {
      "title": "Welcome to the Headless CMS (Edited)",
      "author": "Senior Principal Engineer"
    },
    "status": "Published"
  }
  ```
- **Response**: `200 OK`
- *Note: This action automatically creates a JSON snapshot of the prior record inside the `audit_logs` database before rewriting the row!*

---

## 🌐 Omnichannel API Gateway (The Delivery)

Used by external developers to pull dynamic entries using filtering, pagination, and sorting parameters.

### 1. Fetch Dynamic Collection Content
- **Endpoint**: `GET /api/v1/content/{collection_slug}`
- **Access**: Public
- **Query Parameters**:
  - `status`: Filter by `Published` or `Draft` status.
  - `sort`: Order by columns (e.g. `?sort=-created_at` for descending or `?sort=created_at` for ascending).
  - `limit`: Records per query (default `20`).
  - `offset`: Pagination offset (default `0`).
- **Response**:
  ```json
  {
    "data": [
      {
        "id": "e0b968a3-2c1f-4903-b0f4-5f5cbbda68a3",
        "data": {
          "title": "Welcome to the Headless CMS",
          "author": "Senior Principal Engineer"
        },
        "status": "Published",
        "created_at": "2026-05-29T11:45:00.000000Z",
        "updated_at": "2026-05-29T11:45:00.000000Z"
      }
    ],
    "meta": {
      "total": 1,
      "limit": 20,
      "offset": 0
    }
  }
  ```

---

## 🖼️ Media Upload & Optimization API

Allows editors to upload media assets, auto-compiling them to highly optimized `.webp` formats.

- **Endpoint**: `POST /api/v1/media/upload`
- **Access**: Admin or Editor
- **Payload** (Multipart/Form-Data):
  - `file`: Raw image binary
- **Response**:
  ```json
  {
    "id": "f5f190e3-4c91-49b4-b81b-7a5d3f23a54b",
    "url": "/static/uploads/f5f190e3-4c91-49b4-b81b-7a5d3f23a54b.webp",
    "filename": "f5f190e3-4c91-49b4-b81b-7a5d3f23a54b.webp",
    "mime_type": "image/webp"
  }
  ```
