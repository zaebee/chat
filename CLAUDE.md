# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Backend (Python)
- **Install dependencies**: `uv sync` (recommended)
- **Start legacy chat server**: `python chat.py` (runs on http://localhost:8000)
- **Start Hive ecosystem demo**: `python hive_demo.py` (demonstrates full Hive architecture)
- **Quick Hive demo**: `python hive_demo.py --quick` (fast demonstration)
- **Run tests**: `uv run python -m pytest test_*.py` (run specific test files)
- **Linting**: `uv run ruff check .` (check code style)
- **Format code**: `uv run ruff format .` (auto-format code)
- **Type checking**: `uv run mypy .` (static type analysis)
- **Database**: SQLite database (`chat.db`) is automatically initialized on startup

### Sacred Code Protection (AGRO System)
- **AGRO console scanner**: `python tools/agro_console_scanner.py <files>` (detect console.log violations)
- **Install pre-commit hooks**: `uv run pre-commit install` (sacred protection activation)
- **Run all pre-commit checks**: `uv run pre-commit run --all-files` (manual validation)
- **Sacred Python validation**: `uv run ruff check . && uv run ruff format .` (Python purification)

### Frontend (Vue.js)
- **Install dependencies**: `cd frontend && bun install`
- **Development server**: `cd frontend && bun run dev` (runs on http://localhost:5173)
- **Build for production**: `cd frontend && bun run build`
- **Fast build**: `cd frontend && bun run build-fast` (skip type checking)
- **Type checking**: `cd frontend && bun run type-check`
- **Linting**: `cd frontend && bun run lint`
- **Formatting**: `cd frontend && bun run format`
- **Unit tests**: `cd frontend && bun run test:unit`
- **Preview production build**: `cd frontend && bun run preview`
- **AGRO console scan**: `cd frontend && bun run agro:scan` (detect console.log violations)
- **Sacred validation**: `cd frontend && bun run sacred:validate` (full code purification)
- **Sacred build**: `cd frontend && bun run sacred:build` (blessed production build)

### Hive Ecosystem (New Architecture)
- **Run full demonstration**: `python hive_demo.py`
- **Integration with AI providers**: Set `MISTRAL_API_KEY` and `GEMINI_API_KEY` in `.env` file
- **Component status**: All components implement `get_status()` method for inspection

## Architecture Overview

This is a **"Living Application"** implementing the Beekeeper's Grimoire architectural principles and Hive Constitution governance model. The system has evolved from a simple chat application into a full ecosystem for AI-human collaboration.

### Hive Ecosystem Architecture (New)

The system now implements a complete **Living Hive** with the following components:

**🧬 ATCG Primitives (Grimoire Architecture)**
- **A (Aggregate)**: Structural organization and state management (`hive/primitives.py`)
- **T (Transformation)**: Stateless processing functions for data transformation
- **C (Connector)**: Communication and protocol translation (WebSocket ↔ Pollen Protocol)
- **G (Genesis Event)**: Generative actions and system-wide broadcasting

**🌿 Intent & Physics Levels**
- **Intent Level** (`hive/intent.py`): Philosophical purpose and mission alignment
- **Physics Level** (`hive/physics.py`): Resource constraints and environmental adaptation

**⚡ Pollen Protocol Events** (`hive/events.py`)
- Standardized event system with unique IDs, timestamps, and structured payloads
- Event bus for real-time communication between all components
- Past-tense event types following Constitution requirements

**🤖 AI Teammate Management**
- **HiveRegistry** (`hive/registry.py`): Central management for AI teammates
- **HiveTeammate Interface** (`hive/teammate.py`): Standard interface for all AI agents
- **Welcome Gateway** (`hive/gateway.py`): Metamorphosis-based onboarding (Egg→Larva→Pupa→Adult)

**🎯 Coordination Hub** (`hive/hub.py`)
- Central nervous system orchestrating all components
- Task delegation and load balancing
- Multi-agent collaboration coordination

**📊 Metrics Dashboard** (`hive/dashboard.py`)
- Real-time monitoring of τ (tau), φ (phi), Σ (sigma) metrics
- System health alerts and trend analysis
- Comprehensive reporting for human and AI teammates

**🌐 External AI Integration**
- **Mistral Agent** (`hive/agents/mistral_agent.py`): First external AI teammate
- Extensible framework for Claude, GPT-4, and other AI systems

### Legacy Components (Original Chat App)

**Backend Agent (`chat.py`)**
- FastAPI application with WebSocket support
- Message broadcasting and SQLite persistence
- Static file serving for frontend

**Frontend Agent (`/frontend`)**
- Vue.js 3 SPA with real-time chat interface
- Python playground using Pyodide WebAssembly runtime
- Pinia state management for UI and chat data

### Hive Metrics (τ, φ, Σ)

The system monitors three core metrics following the Grimoire philosophy:

- **τ (tau)**: System complexity and health (lower is better)
- **φ (phi)**: Code quality and maintainability (higher is better)
- **Σ (sigma)**: Collaborative efficiency between teammates

### AI-Human Symbiosis Principles

1. **Legibility**: All components self-describe via `get_status()` methods
2. **Observability**: Structured events and real-time status APIs
3. **Modularity**: Loosely coupled, composable ATCG components
4. **API-First**: Programmatic access to all functionality
5. **Teammate-Friendly**: Designed for both human and AI collaboration

### Development Notes

- **Code Quality**: Always run `uv run ruff check .` and `uv run mypy .` before committing
- **Frontend Development**: Use `bun` for frontend package management (faster than npm)
- **Testing**: Individual test files can be run with `uv run python test_filename.py`
- **Database Initialization**: Run `python -c "from database import init_db; init_db()"` if needed
- **AI Integration**: Both Mistral and Gemini agents are available; configure API keys in `.env`
- **Development Flow**: Start with `python hive_demo.py` to see the complete ecosystem
- **Dual Architecture**: System supports both legacy chat mode and new Hive ecosystem
- **Component Discovery**: All Hive components self-describe via `get_status()` methods