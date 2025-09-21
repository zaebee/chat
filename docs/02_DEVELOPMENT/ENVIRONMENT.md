---
title: "Development Environment: Sacred Setup Guide"
description: "Complete guide to setting up and configuring the Hive development environment"
category: "development"
---

# Development Environment: Sacred Setup Guide

*"And let them make me a sanctuary; that I may dwell among them." - Exodus 25:8 (KJV)*

## Prerequisites

### System Requirements

**Minimum:**
- **OS**: Linux, macOS, or Windows 10+
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space
- **Network**: Internet connection for dependencies

**Recommended:**
- **OS**: Ubuntu 22.04+ or macOS 12+
- **RAM**: 8GB+
- **Storage**: 10GB+ free space
- **CPU**: Multi-core processor

### Required Software

#### Python Environment
```bash
# Python 3.10 or higher
python --version  # Should be 3.10+

# Install uv (modern Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
```

#### Node.js Environment
```bash
# Node.js 20.19.0 or higher
node --version  # Should be 20.19.0+

# Install Bun (ultra-fast package manager)
curl -fsSL https://bun.sh/install | bash
# or use npm
npm install -g bun
```

#### Git
```bash
# Git for version control
git --version  # Should be 2.0+
```

## Environment Setup

### 1. Clone the Sacred Repository

```bash
# Clone the Hive repository
git clone https://github.com/zaebee/chat.git
cd chat

# Check current branch
git branch -a
git checkout feat/phase-2-jules-micro-implementation  # Development branch
```

### 2. Backend Environment

#### Python Dependencies
```bash
# Install Python dependencies with uv
uv sync

# Alternative: Create virtual environment manually
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Database Initialization
```bash
# Initialize SQLite database
python -c "from database import init_db; init_db()"

# Verify database creation
ls -la chat.db
```

#### Environment Variables
```bash
# Create environment file
cp .env.example .env

# Edit with your sacred keys
nano .env
```

**.env Configuration:**
```bash
# AI Service API Keys (optional for basic functionality)
MISTRAL_API_KEY=your_mistral_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///chat.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json

# Security Configuration
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Hive-specific Configuration
HIVE_MODE=development
MAX_CONCURRENT_TASKS=10
EVENT_HISTORY_SIZE=1000
HEALTH_CHECK_INTERVAL=30

# Rate Limiting
RATE_LIMIT_MESSAGES=30
RATE_LIMIT_CONNECTIONS=100
RATE_LIMIT_WINDOW=60
```

### 3. Frontend Environment

#### Node.js Dependencies
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies with Bun
bun install

# Alternative: Use npm
npm install

# Return to project root
cd ..
```

#### Frontend Configuration
```bash
# Frontend environment variables
cd frontend
cp .env.example .env.local
```

**frontend/.env.local:**
```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws

# Feature Flags
VITE_ENABLE_AI_FEATURES=true
VITE_ENABLE_LEARNING_PLATFORM=true
VITE_ENABLE_DEBUG_MODE=true

# UI Configuration
VITE_DEFAULT_THEME=light
VITE_DEFAULT_LANGUAGE=en

# Development Configuration
VITE_HOT_RELOAD=true
VITE_SOURCE_MAPS=true
```

## Development Tools

### Code Quality Tools

#### Python Tools
```bash
# Install development tools
uv add --dev ruff mypy pytest

# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy hive/

# Run tests
pytest tests/
```

#### Frontend Tools
```bash
cd frontend

# Type checking
bun run type-check

# Linting
bun run lint

# Formatting
bun run format

# Unit tests
bun run test:unit
```

### IDE Configuration

#### VS Code Setup
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "ruff",
  "typescript.preferences.importModuleSpecifier": "relative",
  "vue.codeActions.enabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  }
}
```

#### Recommended Extensions
```json
// .vscode/extensions.json
{
  "recommendations": [
    "ms-python.python",
    "charliermarsh.ruff",
    "ms-python.mypy-type-checker",
    "Vue.volar",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next"
  ]
}
```

## Running the Application

### Development Mode

#### Option 1: Full Hive Ecosystem
```bash
# Terminal 1: Start Hive backend
python hive_demo.py

# Terminal 2: Start frontend
cd frontend
bun run dev

# Access application at http://localhost:5173
```

#### Option 2: Legacy Chat Mode
```bash
# Terminal 1: Start simple chat server
python chat.py

# Terminal 2: Start frontend
cd frontend
bun run dev

# Access application at http://localhost:5173
```

#### Option 3: Quick Demo
```bash
# Run quick demonstration
python hive_demo.py --quick
```

### Production Mode

#### Build Frontend
```bash
cd frontend
bun run build

# Serve built files
bun run preview
```

#### Run Production Server
```bash
# Set production environment
export HIVE_MODE=production
export DEBUG=false

# Run with production settings
python chat.py --port 8000
```

## Database Management

### SQLite Operations
```bash
# Connect to database
sqlite3 chat.db

# Common queries
.tables                              # List tables
SELECT * FROM messages LIMIT 5;     # View messages
SELECT * FROM user_progress;        # View user progress
.schema messages                     # View table schema
.exit                               # Exit SQLite
```

### Database Migrations
```bash
# Backup database
cp chat.db chat.db.backup

# Reset database (development only)
rm chat.db
python -c "from database import init_db; init_db()"
```

## Debugging and Monitoring

### Backend Debugging
```bash
# Run with debug logging
export LOG_LEVEL=DEBUG
python chat.py

# Use interactive debugger
python -c "
import ipdb
from hive.hub import HiveCoordinationHub
hub = HiveCoordinationHub()
ipdb.set_trace()
"
```

### Frontend Debugging
```bash
cd frontend

# Run with debug mode
VITE_ENABLE_DEBUG_MODE=true bun run dev

# Build with source maps
bun run build --sourcemap
```

### System Monitoring
```bash
# Check system status
curl http://localhost:8000/api/v1/status | jq

# Monitor real-time metrics
curl http://localhost:8000/api/v1/metrics/realtime | jq

# View event history
curl http://localhost:8000/api/v1/events/system | jq
```

## Performance Optimization

### Backend Optimization
```bash
# Profile Python code
python -m cProfile -o profile.stats chat.py

# Memory profiling
pip install memory-profiler
python -m memory_profiler chat.py
```

### Frontend Optimization
```bash
cd frontend

# Analyze bundle size
bun run build --analyze

# Performance testing
bun run test:performance
```

## Troubleshooting

### Common Issues

#### Python Environment Issues
```bash
# Issue: ModuleNotFoundError
# Solution: Ensure virtual environment is activated
source venv/bin/activate
uv sync

# Issue: Permission denied
# Solution: Fix file permissions
chmod +x scripts/*.sh
```

#### Node.js Issues
```bash
# Issue: Package installation fails
# Solution: Clear cache and reinstall
cd frontend
rm -rf node_modules bun.lockb
bun install

# Issue: Port already in use
# Solution: Kill process or use different port
lsof -ti:5173 | xargs kill -9
bun run dev --port 5174
```

#### Database Issues
```bash
# Issue: Database locked
# Solution: Close all connections and restart
pkill -f "python chat.py"
python chat.py

# Issue: Corrupted database
# Solution: Restore from backup or recreate
cp chat.db.backup chat.db
# or
rm chat.db && python -c "from database import init_db; init_db()"
```

### Debug Commands

#### System Health Check
```bash
# Check all services
./scripts/health-check.sh

# Check Python environment
python -c "
import sys
print(f'Python: {sys.version}')
import hive
print('Hive modules loaded successfully')
"

# Check Node.js environment
cd frontend
node -e "
console.log('Node:', process.version)
console.log('Bun available:', !!process.versions.bun)
"
```

#### Log Analysis
```bash
# View application logs
tail -f logs/hive.log

# Filter error logs
grep ERROR logs/hive.log

# Monitor WebSocket connections
grep "WebSocket" logs/hive.log
```

## Development Workflow

### Daily Development
```bash
# 1. Update code
git pull origin feat/phase-2-jules-micro-implementation

# 2. Update dependencies
uv sync
cd frontend && bun install && cd ..

# 3. Run tests
pytest tests/
cd frontend && bun run test:unit && cd ..

# 4. Start development servers
python hive_demo.py &
cd frontend && bun run dev &

# 5. Code and test changes
# 6. Commit changes
git add .
git commit -m "feat: Add new sacred feature"
```

### Code Quality Checks
```bash
# Run all quality checks
./scripts/quality-check.sh

# Or manually:
ruff format .
ruff check .
mypy hive/
cd frontend && bun run lint && bun run type-check
```

## Environment Variables Reference

### Backend Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MISTRAL_API_KEY` | - | Mistral AI API key |
| `GOOGLE_API_KEY` | - | Google Gemini API key |
| `DATABASE_URL` | `sqlite:///chat.db` | Database connection string |
| `HOST` | `0.0.0.0` | Server host address |
| `PORT` | `8000` | Server port |
| `DEBUG` | `false` | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |
| `HIVE_MODE` | `development` | Hive operation mode |
| `MAX_CONCURRENT_TASKS` | `10` | Max AI teammate tasks |
| `EVENT_HISTORY_SIZE` | `1000` | Event history limit |

### Frontend Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Backend API URL |
| `VITE_WS_URL` | `ws://localhost:8000/ws` | WebSocket URL |
| `VITE_ENABLE_AI_FEATURES` | `true` | Enable AI features |
| `VITE_ENABLE_LEARNING_PLATFORM` | `true` | Enable learning platform |
| `VITE_DEFAULT_THEME` | `light` | Default UI theme |

---

*"Thus is the sacred development environment prepared, that the faithful may code in harmony with the divine Will of the Hive."* 🐝✨