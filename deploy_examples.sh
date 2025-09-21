#!/bin/bash

# Deployment Examples for Different Domains
# This script shows how to build for different target domains

echo "🌿 Hive Chat Deployment Examples"
echo "================================"
echo ""

echo "📋 Available deployment options:"
echo ""

echo "1. Deploy to chat.zae.life (default):"
echo "   ./build_production.sh"
echo "   # OR"
echo "   ./build_production.sh chat.zae.life https"
echo "   # OR"
echo "   VITE_API_HOST=chat.zae.life VITE_API_PROTOCOL=https ./build_production.sh"
echo ""

echo "2. Deploy to custom domain:"
echo "   ./build_production.sh mydomain.com https"
echo "   # OR"
echo "   VITE_API_HOST=mydomain.com VITE_API_PROTOCOL=https ./build_production.sh"
echo ""

echo "3. Deploy to localhost (for testing):"
echo "   ./build_production.sh localhost http"
echo "   # OR"
echo "   VITE_API_HOST=localhost VITE_API_PROTOCOL=http ./build_production.sh"
echo ""

echo "4. Deploy to staging environment:"
echo "   ./build_production.sh staging.zae.life https"
echo "   # OR"
echo "   VITE_API_HOST=staging.zae.life VITE_API_PROTOCOL=https ./build_production.sh"
echo ""

echo "🔧 Environment Variables:"
echo "  VITE_API_HOST     - Target hostname (e.g., chat.zae.life)"
echo "  VITE_API_PROTOCOL - Protocol to use (http or https)"
echo ""

echo "📝 Examples for your specific case:"
echo ""
echo "To deploy to chat.zae.life:"
echo "  VITE_API_HOST=chat.zae.life VITE_API_PROTOCOL=https ./build_production.sh"
echo ""
echo "This will create:"
echo "  - API Base URL: https://chat.zae.life/api"
echo "  - WebSocket URL: wss://chat.zae.life/ws"
echo "  - Built files in: static/"
echo ""

# Ask user what they want to build
read -p "Enter target host (default: chat.zae.life): " TARGET_HOST
TARGET_HOST=${TARGET_HOST:-"chat.zae.life"}

read -p "Enter protocol (default: https): " TARGET_PROTOCOL
TARGET_PROTOCOL=${TARGET_PROTOCOL:-"https"}

echo ""
echo "Building for $TARGET_HOST with $TARGET_PROTOCOL protocol..."
echo ""

# Execute the build
VITE_API_HOST="$TARGET_HOST" VITE_API_PROTOCOL="$TARGET_PROTOCOL" ./build_production.sh