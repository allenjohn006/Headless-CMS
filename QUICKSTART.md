# 🚀 Antigravity Headless CMS - Quick Start Guide

**Enterprise-Grade Headless CMS Engine**  
*Built with FastAPI (Backend) + React/Vite (Frontend)*

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start (2 Commands)](#quick-start-2-commands)
3. [Detailed Setup](#detailed-setup)
4. [Running the System](#running-the-system)
5. [API Endpoints](#api-endpoints)
6. [Default Credentials](#default-credentials)
7. [Troubleshooting](#troubleshooting)

---

## 💻 System Requirements

- **Python**: 3.10+ (tested on 3.14.0)
- **Node.js**: 18+ (tested on 22.20.0)
- **npm**: 7+ (tested on 11.7.0)
- **OS**: Windows, macOS, or Linux
- **Ports Required**: 8002 (Backend), 5173 (Frontend)

### Check Your Versions

```powershell
python --version      # Should be 3.10+
node --version       # Should be 18+
npm --version        # Should be 7+
```

---

## ⚡ Quick Start (2 Commands)

### Option 1: PowerShell (Windows)

**Terminal 1 - Backend:**
```powershell
cd c:\Users\allen\Downloads\CMS\backend ; $env:PYTHONPATH = "$(Get-Location)"; $env:AUTO_CREATE_DB = "True"; python -m uvicorn app.main:app --host 127.0.0.1 --port 8002
```

**Terminal 2 - Frontend:**
```powershell
cd c:\Users\allen\Downloads\CMS\frontend ; npx vite --host 127.0.0.1 --port 5173
```

### Option 2: Bash/Shell (macOS/Linux)

**Terminal 1 - Backend:**
```bash
cd backend
export PYTHONPATH="$(pwd)"
export AUTO_CREATE_DB=True
python -m uvicorn app.main:app --host 127.0.0.1 --port 8002
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npx vite --host 127.0.0.1 --port 5173
```

---

## 📦 Detailed Setup

### 1. Install Backend Dependencies

```powershell
cd c:\Users\allen\Downloads\CMS\backend
pip install -r requirements.txt
```

**Expected packages (13 total):**
- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- alembic
- pydantic + pydantic-settings
- email-validator
- python-jose[cryptography]
- passlib[bcrypt]
- python-multipart
- redis
- Pillow

### 2. Install Frontend Dependencies

```powershell
cd c:\Users\allen\Downloads\CMS\frontend
npm install
```

**Expected packages:**
- React 19.2.6
- React Router DOM 7.16.0
- Vite 8.0.14
- TypeScript 6.0.2
- ESLint + Prettier

---

## 🎯 Running the System

### Full System Startup

You need **two terminal windows** open simultaneously:

#### **Terminal 1: Backend (FastAPI)**

```powershell
# Navigate to backend
cd c:\Users\allen\Downloads\CMS\backend

# Set environment variables
$env:PYTHONPATH = "$(Get-Location)"
$env:AUTO_CREATE_DB = "True"    # Auto-create database on startup
$env:REDIS_ENABLED = "False"    # Optional: Enable Redis caching

# Start the server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8002
```

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
Seeded default admin user: admin@example.com
Seeded default editor user: editor@example.com
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8002 (Press CTRL+C to quit)
```

---

#### **Terminal 2: Frontend (React/Vite)**

```powershell
# Navigate to frontend
cd c:\Users\allen\Downloads\CMS\frontend

# Start dev server
npx vite --host 127.0.0.1 --port 5173
```

**Expected Output:**
```
VITE v8.0.14  ready in 835 ms

  ➜  Local:   http://127.0.0.1:5173/
  ➜  press h + enter to show help
```

---

## 🌐 Access the Application

Once both servers are running, open your browser:

| Component | URL | Purpose |
|-----------|-----|---------|
| **Frontend Dashboard** | http://127.0.0.1:5173 | Admin UI for CMS |
| **API Documentation** | http://127.0.0.1:8002/docs | Interactive Swagger UI |
| **API Health Check** | http://127.0.0.1:8002/health | Server status |
| **OpenAPI Schema** | http://127.0.0.1:8002/openapi.json | API specification |

---

## 🔑 Default Credentials

Use these to log in to the admin dashboard:

### Admin User
```
Email:    admin@example.com
Password: adminpass
Role:     Can create/edit/delete collections, fields, content, media
```

### Editor User
```
Email:    editor@example.com
Password: editorpass
Role:     Can create/edit/delete content and media only
```

---

## 📚 API Endpoints

### Authentication
- **POST** `/api/v1/auth/login` - Get JWT token
- **POST** `/api/v1/auth/register` - Register new user (if enabled)

### Collections (Admin Only)
- **POST** `/api/v1/collections/` - Create collection
- **GET** `/api/v1/collections/` - List all collections
- **DELETE** `/api/v1/collections/{id}` - Delete collection

### Fields (Admin Only)
- **POST** `/api/v1/collections/{collection_id}/fields` - Add field
- **GET** `/api/v1/collections/{collection_id}/fields` - List fields
- **DELETE** `/api/v1/collections/{collection_id}/fields/{field_id}` - Delete field

### Content (Editor+)
- **GET** `/api/v1/content/{collection_slug}` - Get content (public)
- **POST** `/api/v1/content/{collection_slug}` - Create content
- **PUT** `/api/v1/content/{collection_slug}/{content_id}` - Update content
- **DELETE** `/api/v1/content/{collection_slug}/{content_id}` - Delete content

### Media (Editor+)
- **POST** `/api/v1/media/upload` - Upload image (auto-converts to WebP)
- **DELETE** `/api/v1/media/{media_id}` - Delete media

### Health & Status
- **GET** `/health` - System health check
- **GET** `/docs` - Swagger UI documentation

---

## 🛠️ Environment Configuration

Create a `.env` file in the `backend/` directory to customize settings:

```ini
# Environment
ENVIRONMENT=development

# Database
USE_SQLITE=True                    # Set to False for PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=cmsuser
POSTGRES_PASSWORD=cmspassword
POSTGRES_DB=cms_db

# Redis Caching
REDIS_ENABLED=False               # Set to True to enable
REDIS_HOST=localhost
REDIS_PORT=6379
CACHE_TTL_SECONDS=60

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
MIN_PASSWORD_LENGTH=8
ALLOW_PUBLIC_REGISTRATION=False

# Default Users
SEED_DEFAULT_USERS=True
DEFAULT_ADMIN_EMAIL=admin@example.com
DEFAULT_ADMIN_PASSWORD=adminpass
DEFAULT_EDITOR_EMAIL=editor@example.com
DEFAULT_EDITOR_PASSWORD=editorpass

# CORS
CORS_ORIGINS=*                    # Restrict in production

# File Upload
UPLOAD_DIR=uploads

# Database Migration
AUTO_CREATE_DB=True               # Set to False in production
```

---

## 🐘 Using PostgreSQL (Production)

### Step 1: Install PostgreSQL
Download from [postgresql.org](https://www.postgresql.org/download/)

### Step 2: Create Database
```sql
CREATE USER cmsuser WITH PASSWORD 'cmspassword';
CREATE DATABASE cms_db OWNER cmsuser;
```

### Step 3: Update `.env`
```ini
USE_SQLITE=False
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=cmsuser
POSTGRES_PASSWORD=cmspassword
POSTGRES_DB=cms_db
AUTO_CREATE_DB=False
```

### Step 4: Run Migrations
```powershell
cd backend
alembic upgrade head
```

### Step 5: Start Server
```powershell
$env:AUTO_CREATE_DB = "False"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8002
```

---

## ⚡ Enabling Redis Caching

### Step 1: Install Redis
- **Windows**: Download from [microsoft/redis](https://github.com/microsoftarchive/redis/releases)
- **macOS**: `brew install redis`
- **Linux**: `sudo apt-get install redis-server`

### Step 2: Start Redis
```powershell
# Windows
redis-server.exe

# macOS/Linux
redis-server
```

### Step 3: Update `.env`
```ini
REDIS_ENABLED=True
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
CACHE_TTL_SECONDS=300
```

### Step 4: Restart Backend
```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8002
```

---

## 🧪 Testing the API

### Test Authentication
```powershell
$response = Invoke-WebRequest -Uri http://127.0.0.1:8002/api/v1/auth/login `
    -Method POST `
    -ContentType "application/x-www-form-urlencoded" `
    -UseBasicParsing `
    -Body "username=admin@example.com&password=adminpass"

$response.Content | ConvertFrom-Json | Select-Object access_token, token_type
```

### Test Health Check
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8002/health -UseBasicParsing | Select-Object -ExpandProperty Content
```

### Test Collections
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8002/api/v1/collections/ -UseBasicParsing | Select-Object -ExpandProperty Content
```

---

## 🐛 Troubleshooting

### Backend Won't Start

**Error: `ModuleNotFoundError: No module named 'app'`**
```powershell
# Solution: Set PYTHONPATH
$env:PYTHONPATH = "c:\Users\allen\Downloads\CMS\backend"
cd c:\Users\allen\Downloads\CMS\backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8002
```

**Error: `Port 8002 already in use`**
```powershell
# Find and kill process on port 8002
netstat -ano | findstr :8002
taskkill /PID <PID> /F
```

---

### Frontend Won't Start

**Error: `Missing script: "dev"`**
```powershell
# Solution: Use npx directly
cd c:\Users\allen\Downloads\CMS\frontend
npx vite --host 127.0.0.1 --port 5173
```

**Error: `Port 5173 already in use`**
```powershell
# Kill process on port 5173
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

---

### Database Issues

**Error: `no such table: users`**
```powershell
# Solution: Enable auto-create
$env:AUTO_CREATE_DB = "True"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8002
```

**Reset Database (SQLite)**
```powershell
cd c:\Users\allen\Downloads\CMS\backend
Remove-Item cms.db -Force
# Restart server to recreate
```

---

### Authentication Issues

**401 Unauthorized**
- Check that JWT token is included in Authorization header
- Token format: `Authorization: Bearer <token>`
- Tokens expire after 30 minutes (configurable)

**403 Forbidden**
- Admin endpoints require Admin role
- Editor endpoints require Admin or Editor role
- Check user role in database

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────┐
│   React Dashboard (Port 5173)           │
│   - Login UI                            │
│   - Schema Builder                      │
│   - Content Editor                      │
│   - Media Library                       │
└────────────────┬────────────────────────┘
                 │ HTTP + JWT
                 ↓
┌─────────────────────────────────────────┐
│   FastAPI Backend (Port 8002)           │
│   - Authentication                      │
│   - Collections CRUD                    │
│   - Dynamic Content                     │
│   - Media Upload & Optimization         │
│   - Redis Caching (optional)            │
└────────────────┬────────────────────────┘
                 │ SQL
                 ↓
┌─────────────────────────────────────────┐
│   SQLite Database (cms.db)              │
│   - Users, Collections, Fields          │
│   - Content, Audit Logs, Media          │
└─────────────────────────────────────────┘
```

---

## 📝 Development Workflow

1. **Start Backend**: Terminal 1 with `python -m uvicorn ...`
2. **Start Frontend**: Terminal 2 with `npx vite ...`
3. **Make Changes**: Edit code, servers auto-reload
4. **Test API**: Use Swagger UI at `/docs`
5. **View Dashboard**: Open http://127.0.0.1:5173 in browser

---

## 🚢 Production Deployment

For production:

1. **Use PostgreSQL** instead of SQLite
2. **Enable Redis** for caching
3. **Set secure `SECRET_KEY`**
4. **Disable public registration** (`ALLOW_PUBLIC_REGISTRATION=False`)
5. **Run migrations** with `alembic upgrade head`
6. **Use Docker/Docker Compose** (see deployment docs)
7. **Configure proper CORS origins**
8. **Use HTTPS with proper certificates**

---

## 📞 Support

- **API Docs**: http://127.0.0.1:8002/docs
- **GitHub**: [Repository]
- **Issues**: Create an issue for bugs/questions

---

**Happy CMS Building! 🎉**
