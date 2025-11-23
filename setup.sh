#!/bin/bash

# CustomsCompass Setup Script
# This script helps you set up and start the development environment

set -e  # Exit on error

echo "🚀 CustomsCompass Development Setup"
echo "===================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."
echo ""

# Check Docker
if command_exists docker; then
    echo -e "${GREEN}✓${NC} Docker installed: $(docker --version)"
else
    echo -e "${RED}✗${NC} Docker not found"
    echo "  Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check Docker Compose
if docker compose version >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Docker Compose installed: $(docker compose version)"
elif command_exists docker-compose; then
    echo -e "${GREEN}✓${NC} Docker Compose installed: $(docker-compose --version)"
else
    echo -e "${RED}✗${NC} Docker Compose not found"
    echo "  Please install Docker Compose"
    exit 1
fi

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} Python installed: $PYTHON_VERSION"

    # Check if Python version is 3.11+
    if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 11) else 1)'; then
        echo -e "  ${GREEN}Python 3.11+ detected${NC}"
    else
        echo -e "  ${YELLOW}Warning: Python 3.11+ recommended, you have $PYTHON_VERSION${NC}"
    fi
else
    echo -e "${RED}✗${NC} Python not found"
    echo "  Please install Python 3.11+ from: https://www.python.org/downloads/"
    exit 1
fi

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js installed: $NODE_VERSION"

    # Check if Node version is 18+
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_MAJOR" -ge 18 ]; then
        echo -e "  ${GREEN}Node.js 18+ detected${NC}"
    else
        echo -e "  ${YELLOW}Warning: Node.js 18+ recommended, you have $NODE_VERSION${NC}"
    fi
else
    echo -e "${RED}✗${NC} Node.js not found"
    echo "  Please install Node.js 18+ from: https://nodejs.org/"
    exit 1
fi

# Check npm
if command_exists npm; then
    echo -e "${GREEN}✓${NC} npm installed: $(npm --version)"
else
    echo -e "${RED}✗${NC} npm not found"
    exit 1
fi

echo ""
echo "✅ All prerequisites met!"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠${NC}  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo -e "${GREEN}✓${NC} Created .env file"
    echo -e "${YELLOW}⚠${NC}  Please update .env with your SECRET_KEY and other settings"
    echo ""
    echo "Generate a secure SECRET_KEY with:"
    echo "  openssl rand -hex 32"
    echo ""
fi

# Step 1: Start Docker services
echo "📦 Step 1: Starting Docker services..."
echo ""

COMPOSE_CMD="docker compose"
if ! docker compose version >/dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
fi

$COMPOSE_CMD up -d

echo ""
echo "Waiting for services to be ready..."
sleep 5

# Check if services are running
if $COMPOSE_CMD ps | grep -q "Up"; then
    echo -e "${GREEN}✓${NC} Docker services started successfully"
else
    echo -e "${RED}✗${NC} Failed to start Docker services"
    $COMPOSE_CMD ps
    exit 1
fi

echo ""
echo "Docker services status:"
$COMPOSE_CMD ps

# Step 2: Setup backend
echo ""
echo "🐍 Step 2: Setting up Python backend..."
echo ""

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓${NC} Python dependencies installed"

cd ..

# Step 3: Setup frontend
echo ""
echo "⚛️  Step 3: Setting up Next.js frontend..."
echo ""

cd frontend

# Install npm dependencies
echo "Installing npm dependencies (this may take a few minutes)..."
npm install
echo -e "${GREEN}✓${NC} npm dependencies installed"

cd ..

# Success!
echo ""
echo "🎉 Setup complete!"
echo ""
echo "===================================="
echo "Next steps:"
echo "===================================="
echo ""
echo "1. Start the backend (in one terminal):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn main:app --reload"
echo ""
echo "2. Start the frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Access your applications:"
echo "   Frontend:     http://localhost:3000"
echo "   Backend API:  http://localhost:8000"
echo "   API Docs:     http://localhost:8000/api/docs"
echo "   PostgreSQL:   localhost:5432 (customs/customs)"
echo "   Redis:        localhost:6379"
echo "   MinIO:        http://localhost:9001 (minioadmin/minioadmin)"
echo "   Mailhog:      http://localhost:8025"
echo ""
echo "===================================="
echo "Useful commands:"
echo "===================================="
echo ""
echo "Stop Docker services:"
echo "  $COMPOSE_CMD down"
echo ""
echo "View Docker logs:"
echo "  $COMPOSE_CMD logs -f"
echo ""
echo "Restart a service:"
echo "  $COMPOSE_CMD restart postgres"
echo ""
