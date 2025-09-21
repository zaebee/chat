# 🐝 Hive Chat Deployment Guide

This guide provides instructions for deploying the Hive Chat "Living Application" to production environments, including chat.zae.life.

## 🚀 Quick Deployment (Production Ready)

### Prerequisites

- **Python 3.12+** with uv package manager
- **Node.js 20+** with bun runtime
- **Domain with SSL** (e.g., chat.zae.life)
- **Reverse proxy** (nginx/caddy recommended)
- **Process manager** (systemd/pm2/supervisor)

### 1. Server Setup

```bash
# Clone repository
git clone https://github.com/zaebee/chat.git
cd chat

# Install Python dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv sync

# Install Node.js dependencies
curl -fsSL https://bun.sh/install | bash
export PATH="$HOME/.bun/bin:$PATH"
cd frontend && bun install && cd ..

# Initialize database
uv run python -c "from database import init_db; init_db()"
```

### 2. Environment Configuration

Create `.env` file:

```bash
# API Keys (optional but recommended)
MISTRAL_API_KEY=your_mistral_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Production settings
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
DATABASE_PATH=./chat.db

# Security (generate strong secrets)
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=https://chat.zae.life,https://www.chat.zae.life
```

### 3. Build Frontend

```bash
cd frontend
bun run build
cd ..

# Copy built files to static directory
cp -r frontend/dist/* static/
```

### 4. Production Server

Create `production_server.py`:

```python
#!/usr/bin/env python3
"""
Production server for Hive Chat
"""

import uvicorn
import os
from hive_chat import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        workers=1,  # Single worker for WebSocket support
        access_log=True,
        log_level="info"
    )
```

### 5. Systemd Service

Create `/etc/systemd/system/hive-chat.service`:

```ini
[Unit]
Description=Hive Chat Living Application
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/hive-chat
Environment=PATH=/opt/hive-chat/.venv/bin
ExecStart=/opt/hive-chat/.venv/bin/python production_server.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable hive-chat
sudo systemctl start hive-chat
sudo systemctl status hive-chat
```

### 6. Nginx Configuration

Create `/etc/nginx/sites-available/chat.zae.life`:

```nginx
server {
    listen 80;
    server_name chat.zae.life www.chat.zae.life;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name chat.zae.life www.chat.zae.life;

    # SSL Configuration (use certbot for Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/chat.zae.life/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/chat.zae.life/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Proxy to Hive Chat
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }

    # Static files (if serving separately)
    location /static/ {
        alias /opt/hive-chat/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API endpoints
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket endpoint
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/chat.zae.life /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Install Node.js and bun
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN uv sync
RUN cd frontend && bun install && bun run build && cd ..

# Initialize database
RUN uv run python -c "from database import init_db; init_db()"

# Copy built frontend to static
RUN cp -r frontend/dist/* static/

# Expose port
EXPOSE 8000

# Run application
CMD ["uv", "run", "python", "hive_chat.py", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  hive-chat:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - HOST=0.0.0.0
      - PORT=8000
    volumes:
      - ./data:/app/data
      - ./.env:/app/.env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - /etc/letsencrypt:/etc/letsencrypt
    depends_on:
      - hive-chat
    restart: unless-stopped
```

## 🔧 Development Deployment

For development/testing on chat.zae.life:

```bash
# Quick start
git clone https://github.com/zaebee/chat.git
cd chat

# Install dependencies
uv sync
cd frontend && bun install && cd ..

# Run development servers
# Terminal 1: Backend
uv run python hive_chat.py --port 8000

# Terminal 2: Frontend (if developing)
cd frontend && bun run dev --port 5173
```

## 📊 Monitoring & Health Checks

### Health Endpoints

- **System Status**: `GET /api/v1/status`
- **Health Check**: `GET /api/v1/health`
- **Metrics**: `GET /api/v1/metrics`

### Example Health Check Script

```bash
#!/bin/bash
# health_check.sh

HEALTH_URL="https://chat.zae.life/api/v1/health"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $STATUS -eq 200 ]; then
    echo "✅ Hive Chat is healthy"
    exit 0
else
    echo "❌ Hive Chat is unhealthy (HTTP $STATUS)"
    exit 1
fi
```

### Monitoring with systemd

```bash
# Check service status
sudo systemctl status hive-chat

# View logs
sudo journalctl -u hive-chat -f

# Restart if needed
sudo systemctl restart hive-chat
```

## 🔐 Security Considerations

### 1. Environment Variables

Never commit sensitive data. Use environment variables:

```bash
# .env (never commit this file)
MISTRAL_API_KEY=sk-...
GEMINI_API_KEY=...
SECRET_KEY=...
```

### 2. Firewall Configuration

```bash
# Allow only necessary ports
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 3. SSL/TLS Setup

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d chat.zae.life -d www.chat.zae.life

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🚀 Performance Optimization

### 1. Static File Serving

Serve static files directly through nginx for better performance.

### 2. Database Optimization

For production, consider upgrading from SQLite to PostgreSQL:

```python
# In production_settings.py
DATABASE_URL = "postgresql://user:pass@localhost/hivedb"
```

### 3. Caching

Add Redis for session management and caching:

```bash
sudo apt install redis-server
```

## 📈 Scaling Considerations

### Horizontal Scaling

For multiple instances, use:

1. **Load Balancer** (nginx/haproxy)
2. **Shared Database** (PostgreSQL)
3. **Session Store** (Redis)
4. **Message Queue** (Redis/RabbitMQ)

### Vertical Scaling

Monitor resource usage:

```bash
# CPU and memory usage
htop

# Disk usage
df -h

# Network connections
netstat -an | grep :8000
```

## 🐝 Hive-Specific Features

### AI Agent Configuration

Add API keys for AI agents:

```bash
# .env
MISTRAL_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here  # For future Claude integration
```

### Event Bus Monitoring

Monitor the Pollen Protocol events:

```bash
# Check event bus status
curl https://chat.zae.life/api/v1/status | jq '.data.event_bus_status'
```

### Agent Health

Monitor AI agent health:

```bash
# List active agents
curl https://chat.zae.life/api/v1/agents

# Check specific agent
curl https://chat.zae.life/api/v1/agents/mistral_agent
```

## 🆘 Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Check nginx WebSocket proxy configuration
   - Verify firewall allows connections

2. **Database Locked**
   - Ensure only one instance is running
   - Check file permissions on chat.db

3. **AI Agents Not Responding**
   - Verify API keys in environment
   - Check agent status via `/api/v1/agents`

4. **High Memory Usage**
   - Monitor with `htop`
   - Consider restarting service periodically

### Log Analysis

```bash
# Application logs
sudo journalctl -u hive-chat -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# System resources
dmesg | tail
```

## 📞 Support

For deployment issues:

1. Check the [GitHub Issues](https://github.com/zaebee/chat/issues)
2. Review the [Documentation](docs/README.md)
3. Monitor system health via `/api/v1/health`

---

**🐝 Welcome to the Living Application ecosystem!**

This deployment creates a self-contained, self-organizing system that demonstrates the future of human-AI collaboration. The Hive Chat will continue to evolve and adapt as more AI teammates join the ecosystem.