# 🚀 Hive Chat Deployment Guide

## Environment Variables for Domain Configuration

You can configure the target domain and protocol using environment variables:

### Available Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `VITE_API_HOST` | Target hostname | `chat.zae.life` | `mydomain.com` |
| `VITE_API_PROTOCOL` | Protocol (http/https) | `https` | `https` |
| `VITE_FORCE_PRODUCTION` | Force production mode | `true` (auto-set) | `true` |

## Deployment Methods

### Method 1: Command Line Arguments
```bash
./build_production.sh [HOST] [PROTOCOL]
```

**Examples:**
```bash
# Deploy to chat.zae.life (default)
./build_production.sh

# Deploy to chat.zae.life explicitly
./build_production.sh chat.zae.life https

# Deploy to custom domain
./build_production.sh mydomain.com https

# Deploy to localhost for testing
./build_production.sh localhost http
```

### Method 2: Environment Variables
```bash
VITE_API_HOST=hostname VITE_API_PROTOCOL=protocol ./build_production.sh
```

**Examples:**
```bash
# Deploy to chat.zae.life
VITE_API_HOST=chat.zae.life VITE_API_PROTOCOL=https ./build_production.sh

# Deploy to custom domain
VITE_API_HOST=mydomain.com VITE_API_PROTOCOL=https ./build_production.sh

# Deploy to staging
VITE_API_HOST=staging.zae.life VITE_API_PROTOCOL=https ./build_production.sh
```

### Method 3: Interactive Script
```bash
./deploy_examples.sh
```
This script will prompt you for the target domain and protocol.

## For Your Specific Case (chat.zae.life)

To deploy to **chat.zae.life**, use any of these commands:

```bash
# Option 1: Default (no arguments needed)
./build_production.sh

# Option 2: Explicit arguments
./build_production.sh chat.zae.life https

# Option 3: Environment variables
VITE_API_HOST=chat.zae.life VITE_API_PROTOCOL=https ./build_production.sh
```

## Build Output

After building, you'll get:

- **API Base URL**: `https://chat.zae.life/api`
- **WebSocket URL**: `wss://chat.zae.life/ws`
- **Built files**: `frontend/dist/`
- **Deployed to**: `static/`
- **Deployment info**: `static/deployment-info.json`

## Verification

Check the deployment info file to verify the configuration:

```bash
cat static/deployment-info.json
```

Example output:
```json
{
  "buildTime": "2025-09-21T06:00:00Z",
  "targetHost": "chat.zae.life",
  "protocol": "https",
  "websocketUrl": "wss://chat.zae.life/ws",
  "apiBaseUrl": "https://chat.zae.life/api",
  "buildType": "production",
  "deploymentTarget": "chat.zae.life",
  "environmentVariables": {
    "VITE_API_HOST": "chat.zae.life",
    "VITE_API_PROTOCOL": "https"
  }
}
```

## Environment Detection

The frontend uses build-time configuration to determine the target:

- **Build-time variables set**: Uses production mode with specified target (recommended)
- **No build-time variables**: Falls back to runtime detection for development
- **Force production**: `VITE_FORCE_PRODUCTION=true` overrides runtime detection

**Important**: When you run `./build_production.sh`, it automatically sets `VITE_FORCE_PRODUCTION=true` to ensure the build targets the specified domain, even when building in development environments like Gitpod.

## Quick Reference

| Task | Command |
|------|---------|
| Deploy to chat.zae.life | `./build_production.sh` |
| Deploy to custom domain | `./build_production.sh mydomain.com https` |
| Interactive deployment | `./deploy_examples.sh` |
| Check deployment info | `cat static/deployment-info.json` |