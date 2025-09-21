#!/bin/bash

# Production Build Script with Configurable Domain
# Usage: ./build_production.sh [HOST] [PROTOCOL]
# Example: ./build_production.sh chat.zae.life https

set -e

# Parse command line arguments or use environment variables
TARGET_HOST=${1:-${VITE_API_HOST:-"chat.zae.life"}}
TARGET_PROTOCOL=${2:-${VITE_API_PROTOCOL:-"https"}}

# Export for Vite build process
export VITE_API_HOST="$TARGET_HOST"
export VITE_API_PROTOCOL="$TARGET_PROTOCOL"
export VITE_FORCE_PRODUCTION="true"

echo "🌿 Building Hive Chat Frontend for $TARGET_HOST ($TARGET_PROTOCOL)..."

# Navigate to frontend directory
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    ~/.bun/bin/bun install
fi

# Build for production
echo "🔨 Building production bundle for chat.zae.life..."
~/.bun/bin/bun run build

# Navigate back to root
cd ..

# Copy built files to static directory
echo "📁 Copying build to static directory..."
rm -rf static/assets static/index.html 2>/dev/null || true
cp -r frontend/dist/* static/

# Determine WebSocket protocol
WS_PROTOCOL="ws"
if [ "$TARGET_PROTOCOL" = "https" ]; then
    WS_PROTOCOL="wss"
fi

# Create deployment info file
cat > static/deployment-info.json << EOF
{
  "buildTime": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "targetHost": "$TARGET_HOST",
  "protocol": "$TARGET_PROTOCOL",
  "websocketUrl": "$WS_PROTOCOL://$TARGET_HOST/ws",
  "apiBaseUrl": "$TARGET_PROTOCOL://$TARGET_HOST/api",
  "buildType": "production",
  "deploymentTarget": "$TARGET_HOST",
  "environmentVariables": {
    "VITE_API_HOST": "$VITE_API_HOST",
    "VITE_API_PROTOCOL": "$VITE_API_PROTOCOL",
    "VITE_FORCE_PRODUCTION": "$VITE_FORCE_PRODUCTION"
  }
}
EOF

echo "✅ Frontend build complete for $TARGET_HOST!"
echo ""
echo "📋 Deployment Summary:"
echo "  - Target: $TARGET_PROTOCOL://$TARGET_HOST"
echo "  - Built files: frontend/dist/"
echo "  - Copied to: static/"
echo "  - WebSocket: $WS_PROTOCOL://$TARGET_HOST/ws"
echo "  - API Base: $TARGET_PROTOCOL://$TARGET_HOST/api"
echo ""
echo "🚀 Ready for deployment to $TARGET_HOST"
echo "   Frontend configured for $TARGET_PROTOCOL protocol"
echo "   All API calls will target $TARGET_HOST domain"