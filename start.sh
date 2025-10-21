#!/bin/bash

# FastAPI Application Startup Script

echo "🚀 Starting FastAPI Task Management Application with PostgreSQL"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command_exists docker; then
    echo -e "${RED}❌ Docker is required but not installed.${NC}"
    exit 1
fi

if ! command_exists docker-compose; then
    echo -e "${RED}❌ Docker Compose is required but not installed.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Start PostgreSQL container
echo -e "${BLUE}Starting PostgreSQL container...${NC}"
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
echo -e "${YELLOW}⏳ Waiting for PostgreSQL to be ready...${NC}"
timeout=30
counter=0

while ! docker-compose exec postgres pg_isready -U taskuser -d taskdb >/dev/null 2>&1; do
    if [ $counter -ge $timeout ]; then
        echo -e "${RED}❌ PostgreSQL failed to start within $timeout seconds${NC}"
        exit 1
    fi
    sleep 1
    counter=$((counter + 1))
    echo -n "."
done

echo -e "\n${GREEN}✅ PostgreSQL is ready!${NC}"

# Install Python dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Start the FastAPI application
echo -e "${BLUE}Starting FastAPI application...${NC}"
echo -e "${GREEN}🌟 Application will be available at: http://localhost:8000${NC}"
echo -e "${GREEN}📚 API Documentation: http://localhost:8000/docs${NC}"
echo -e "${GREEN}🔧 PgAdmin (optional): http://localhost:5050${NC}"
echo -e "${YELLOW}   PgAdmin credentials: admin@admin.com / admin${NC}"

# Start the application
cd app && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000