#!/bin/bash

# SocialSeed v2.0 - Startup Script
# Enterprise Social Media Orchestration with Phased Safety Approach

echo "🚀 Starting SocialSeed v2.0..."
echo "=================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp backend/.env.example backend/.env
    echo "📝 Please edit backend/.env with your API keys before continuing."
    echo "   Required keys: DEEPSEEK_API_KEY, DATABASE_URL"
    echo ""
    read -p "Press Enter after editing .env file to continue..."
fi

# Create logs directory if it doesn't exist
mkdir -p logs

echo "🔧 Starting services with Docker Compose..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
echo "=================="

# Check PostgreSQL
if docker-compose ps postgres | grep -q "Up"; then
    echo "✅ PostgreSQL: Running"
else
    echo "❌ PostgreSQL: Failed to start"
fi

# Check Redis
if docker-compose ps redis | grep -q "Up"; then
    echo "✅ Redis: Running"
else
    echo "❌ Redis: Failed to start"
fi

# Check Backend
if docker-compose ps backend | grep -q "Up"; then
    echo "✅ Backend API: Running"
else
    echo "❌ Backend API: Failed to start"
fi

# Check Frontend
if docker-compose ps frontend | grep -q "Up"; then
    echo "✅ Frontend: Running"
else
    echo "❌ Frontend: Failed to start"
fi

echo ""
echo "🌐 Access URLs:"
echo "==============="
echo "Dashboard:     http://localhost:3000"
echo "API:          http://localhost:8000"
echo "Database:     localhost:5432"
echo "Redis:        localhost:6379"
echo ""

echo "📋 Useful Commands:"
echo "==================="
echo "View logs:        docker-compose logs -f"
echo "Stop services:    docker-compose down"
echo "Restart:          docker-compose restart"
echo "Update:           docker-compose pull && docker-compose up -d"
echo ""

echo "🎯 Next Steps:"
echo "=============="
echo "1. Open http://localhost:3000 in your browser"
echo "2. Review the dashboard and system status"
echo "3. Check pending approvals if any exist"
echo "4. Monitor platform health indicators"
echo "5. Start with Phase 1 (ultra-conservative approach)"
echo ""

echo "🚀 SocialSeed v2.0 is ready! Happy growing! 🚀"

