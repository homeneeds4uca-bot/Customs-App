# 🪟 CustomsCompass - Windows Setup Guide

Complete guide for setting up CustomsCompass on Windows at:
`C:\Users\siruv\OneDrive\Documents\DATA1\AI Apps\Customs 2.0 - Claude Code`

## Prerequisites for Windows

### 1. Install Required Software

**Docker Desktop** (Required)
- Download: https://www.docker.com/products/docker-desktop/
- Install and restart your computer
- Enable WSL 2 backend when prompted
- Open Docker Desktop and let it start completely

**Python 3.11+** (Required)
- Download: https://www.python.org/downloads/
- ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
- Verify: Open PowerShell and run `python --version`

**Node.js 18+** (Required)
- Download: https://nodejs.org/ (LTS version)
- Install with default settings
- Verify: Open PowerShell and run `node --version`

**Git for Windows** (Required)
- Download: https://git-scm.com/download/win
- Install with default settings
- Verify: Open PowerShell and run `git --version`

**Visual Studio Code** (Recommended)
- Download: https://code.visualstudio.com/
- Recommended extensions:
  - Python
  - ESLint
  - Prettier
  - Tailwind CSS IntelliSense

## Getting the Code

### Option 1: Clone from GitHub (Recommended)

Open **PowerShell** as Administrator and run:

```powershell
# Navigate to your desired location
cd "C:\Users\siruv\OneDrive\Documents\DATA1\AI Apps"

# Clone the repository
git clone https://github.com/homeneeds4uca-bot/Customs-App.git "Customs 2.0 - Claude Code"

# Navigate into the project
cd "Customs 2.0 - Claude Code"

# Checkout the development branch
git checkout claude/customscompass-saas-platform-01Moe1jN1xbcZeSNv5qTKDWw
```

### Option 2: Download and Extract Archive

If you have the `CustomsCompass-Complete.tar.gz` file:

1. Install **7-Zip** (https://www.7-zip.org/) if not already installed
2. Right-click the `.tar.gz` file → 7-Zip → Extract Here
3. Move the extracted `Customs-App` folder to:
   `C:\Users\siruv\OneDrive\Documents\DATA1\AI Apps\Customs 2.0 - Claude Code`

## Setup on Windows

### Step 1: Environment Configuration

Open PowerShell in your project directory:

```powershell
cd "C:\Users\siruv\OneDrive\Documents\DATA1\AI Apps\Customs 2.0 - Claude Code"

# Copy environment template
Copy-Item .env.example .env

# Edit .env file
notepad .env
```

In the `.env` file, update the `SECRET_KEY`:

```
SECRET_KEY=your-generated-key-here
```

Generate a secure key using PowerShell:
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})
```

Copy the output and paste it as your `SECRET_KEY` in `.env`

### Step 2: Start Docker Services

**Important**: Make sure Docker Desktop is running!

```powershell
# Start all services
docker compose up -d

# Wait 10 seconds for services to start
Start-Sleep -Seconds 10

# Check services are running
docker compose ps
```

You should see:
- ✅ customs_postgres
- ✅ customs_redis
- ✅ customs_minio
- ✅ customs_mailhog

### Step 3: Setup Backend

Open a new PowerShell terminal:

```powershell
cd "C:\Users\siruv\OneDrive\Documents\DATA1\AI Apps\Customs 2.0 - Claude Code\backend"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Setup Frontend

Open another new PowerShell terminal:

```powershell
cd "C:\Users\siruv\OneDrive\Documents\DATA1\AI Apps\Customs 2.0 - Claude Code\frontend"

# Install dependencies (this may take a few minutes)
npm install
```

### Step 5: Start Development Servers

**Terminal 1 - Backend:**

```powershell
cd "C:\Users\siruv\OneDrive\Documents\DATA1\AI Apps\Customs 2.0 - Claude Code\backend"
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**

```powershell
cd "C:\Users\siruv\OneDrive\Documents\DATA1\AI Apps\Customs 2.0 - Claude Code\frontend"
npm run dev
```

## Verification

Open your web browser and test:

| Service | URL | Expected Result |
|---------|-----|-----------------|
| Frontend | http://localhost:3000 | CustomsCompass landing page |
| Backend API | http://localhost:8000 | JSON response with app info |
| API Docs | http://localhost:8000/api/docs | Swagger UI |
| MinIO Console | http://localhost:9001 | Login page (minioadmin/minioadmin) |
| Mailhog | http://localhost:8025 | Email testing interface |

## Troubleshooting Windows-Specific Issues

### Issue: "Execution Policy" Error

**Error:** `cannot be loaded because running scripts is disabled`

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Docker Connection Refused

**Error:** `Cannot connect to Docker daemon`

**Solution:**
1. Open Docker Desktop
2. Wait for it to fully start (whale icon should be steady)
3. Run `docker ps` to verify Docker is running
4. Try `docker compose up -d` again

### Issue: Port Already in Use

**Error:** `port is already allocated`

**Solution:**
```powershell
# Check what's using port 5432 (PostgreSQL)
netstat -ano | findstr :5432

# Find the process ID (last column) and kill it:
taskkill /PID <process_id> /F

# Or change the port in docker-compose.yml
```

### Issue: PostgreSQL Connection Refused

**Solution:**
```powershell
# Restart PostgreSQL container
docker compose restart postgres

# Check logs
docker compose logs postgres

# If still failing, recreate the container
docker compose down
docker compose up -d
```

### Issue: npm install fails

**Solution:**
```powershell
cd frontend

# Clear npm cache
npm cache clean --force

# Delete node_modules if it exists
Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue

# Delete package-lock.json if it exists
Remove-Item package-lock.json -ErrorAction SilentlyContinue

# Install again
npm install
```

### Issue: Python ModuleNotFoundError

**Solution:**
```powershell
cd backend

# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

## Useful PowerShell Commands

### Docker Management

```powershell
# Stop all services
docker compose down

# Stop and remove all data (clean slate)
docker compose down -v

# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f postgres

# Restart a service
docker compose restart postgres

# Check service status
docker compose ps

# Access PostgreSQL directly
docker exec -it customs_postgres psql -U customs -d customs_compass
```

### Python Virtual Environment

```powershell
# Activate
.\venv\Scripts\Activate.ps1

# Deactivate
deactivate

# Check installed packages
pip list

# Update a package
pip install --upgrade <package-name>
```

### Git Operations

```powershell
# Check current branch
git branch

# Pull latest changes
git pull origin claude/customscompass-saas-platform-01Moe1jN1xbcZeSNv5qTKDWw

# Check status
git status

# View commit history
git log --oneline
```

## VS Code Setup

### Open in VS Code

```powershell
cd "C:\Users\siruv\OneDrive\Documents\DATA1\AI Apps\Customs 2.0 - Claude Code"
code .
```

### Recommended Settings

Create `.vscode\settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}\\backend\\venv\\Scripts\\python.exe",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.pytest_cache": true,
    "**/node_modules": true,
    "**/.next": true
  }
}
```

## Next Steps

1. ✅ All services running and verified
2. 📝 Explore the API at http://localhost:8000/api/docs
3. 🎨 Check the landing page at http://localhost:3000
4. 📧 Test email sending via Mailhog at http://localhost:8025
5. 🗄️ Connect to PostgreSQL:
   - Host: localhost
   - Port: 5432
   - Database: customs_compass
   - User: customs
   - Password: customs
6. 🚀 Start building features!

## Quick Reference

**Project Location:**
```
C:\Users\siruv\OneDrive\Documents\DATA1\AI Apps\Customs 2.0 - Claude Code
```

**Start Everything:**
1. Open Docker Desktop
2. Terminal 1: `docker compose up -d`
3. Terminal 2: Backend → Activate venv → `uvicorn main:app --reload`
4. Terminal 3: Frontend → `npm run dev`

**Stop Everything:**
1. Ctrl+C in backend terminal
2. Ctrl+C in frontend terminal
3. `docker compose down`

## Support

- **Backend docs**: `backend\README.md`
- **General docs**: `README.md`
- **Quick start**: `QUICKSTART.md`
- **API reference**: http://localhost:8000/api/docs

---

**🎉 You're all set! Happy coding! 🇨🇦**
