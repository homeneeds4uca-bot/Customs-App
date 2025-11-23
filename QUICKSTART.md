# 🚀 CustomsCompass Quick Start Guide

This guide will get you up and running in under 5 minutes.

## Prerequisites

Before you begin, ensure you have:

- **Docker Desktop** (includes Docker Compose) - [Download](https://docs.docker.com/get-docker/)
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)

## Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
./setup.sh
```

This will:
1. ✓ Check all prerequisites
2. ✓ Create `.env` file if needed
3. ✓ Start Docker services
4. ✓ Install Python dependencies
5. ✓ Install npm dependencies

Then follow the on-screen instructions to start the servers.

## Option 2: Manual Setup

### Step 1: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Generate a secure SECRET_KEY
openssl rand -hex 32

# Edit .env and paste the generated key
nano .env
```

### Step 2: Start Docker Services

```bash
docker compose up -d
```

Verify services are running:

```bash
docker compose ps
```

You should see:
- ✓ customs_postgres (port 5432)
- ✓ customs_redis (port 6379)
- ✓ customs_minio (ports 9000, 9001)
- ✓ customs_mailhog (ports 1025, 8025)

### Step 3: Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Setup Frontend

```bash
cd frontend

# Install dependencies
npm install
```

### Step 5: Start Development Servers

**Terminal 1 - Backend:**

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

You should see:
```
✓ CustomsCompass v1.0.0 started
✓ Environment: development
✓ Database: localhost:5432/customs_compass
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

You should see:
```
✓ Ready on http://localhost:3000
```

## 🌐 Access Your Applications

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | Landing page and user interface |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs (Swagger)** | http://localhost:8000/api/docs | Interactive API documentation |
| **PostgreSQL** | localhost:5432 | Database (user: customs, password: customs) |
| **Redis** | localhost:6379 | Cache and sessions |
| **MinIO Console** | http://localhost:9001 | S3-compatible storage (admin/admin) |
| **Mailhog UI** | http://localhost:8025 | Email testing interface |

## ✅ Verification

### Test Backend

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","version":"1.0.0"}
```

### Test Frontend

Open http://localhost:3000 in your browser. You should see the CustomsCompass landing page.

### Test Database Connection

```bash
docker exec -it customs_postgres psql -U customs -d customs_compass -c "\dt"
```

You should see a list of database tables (users, products, classifications, etc.).

## 🐛 Troubleshooting

### Frontend won't start

**Error:** `Module not found: Can't resolve '@radix-ui/react-avatar'`

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Docker services won't start

**Error:** `port is already allocated`

**Solution:**
```bash
# Stop conflicting services
docker compose down

# Check what's using the port
lsof -i :5432  # For PostgreSQL
lsof -i :6379  # For Redis

# Kill the process or change ports in docker-compose.yml
```

### Database connection refused

**Error:** `could not connect to server: Connection refused`

**Solution:**
```bash
# Restart PostgreSQL
docker compose restart postgres

# Check logs
docker compose logs postgres

# Verify it's running
docker compose ps
```

### Can't access MinIO Console

**Solution:**
```bash
# Restart MinIO
docker compose restart minio

# Access at http://localhost:9001
# Default credentials: minioadmin/minioadmin
```

## 🔧 Useful Commands

### Docker

```bash
# Stop all services
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v

# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f postgres

# Restart a service
docker compose restart postgres

# Check service status
docker compose ps
```

### Backend

```bash
# Run tests
cd backend
source venv/bin/activate
pytest

# Check for type errors
mypy .

# Format code
black .

# Start with different port
uvicorn main:app --reload --port 8001
```

### Frontend

```bash
# Run tests
npm test

# Type check
npm run type-check

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## 📚 Next Steps

1. **Explore the API**
   - Visit http://localhost:8000/api/docs
   - Try the `/api/auth/register` endpoint
   - Create a test user account

2. **Check the Database**
   - Connect with your favorite PostgreSQL client
   - Host: localhost, Port: 5432
   - Database: customs_compass
   - User: customs, Password: customs

3. **Test Email Sending**
   - Register a new user
   - Check Mailhog at http://localhost:8025
   - You should see the verification email

4. **Start Development**
   - Backend code is in `backend/`
   - Frontend code is in `frontend/`
   - See main README.md for architecture details

## 🆘 Need Help?

- **Backend issues**: Check `backend/README.md`
- **Frontend issues**: Check `frontend/README.md`
- **Architecture**: See main `README.md`
- **API Reference**: http://localhost:8000/api/docs

## 🎉 You're Ready!

Your CustomsCompass development environment is now running. Happy coding! 🇨🇦
