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

- **Sacred AGRO Scanner**: `python tools/agro_scanner.py <files>` (Sacred Gateway to ATCG architecture)
- **Sacred self-assessment**: `python tools/agro_scanner.py --self-check` (scan AGRO system itself)
- **ATCG component status**: `python tools/agro_scanner.py --status` (view Sacred Architecture status)
- **Pure ATCG interface**: `python -m tools.agro.sacred_scanner <files>` (direct Inner Sanctum access)
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
- **AGRO console scan**: `cd frontend && python ../tools/agro_scanner.py $(find src -name '*.vue' -o -name '*.ts' -o -name '*.js')` (Sacred ATCG scan)
- **Sacred validation**: `cd frontend && bun run sacred:validate` (full code purification)
- **Sacred build**: `cd frontend && bun run sacred:build` (blessed production build)

### Hive Ecosystem (New Architecture)

- **Run full demonstration**: `python hive_demo.py`
- **Integration with AI providers**: Set `MISTRAL_API_KEY` and `GEMINI_API_KEY` in `.env` file
- **Component status**: All components implement `get_status()` method for inspection

## Architecture Overview

This is a **"Living Application"** implementing the Beekeeper's Grimoire architectural principles and Hive Constitution governance model. The system has evolved from a simple chat application into a full ecosystem for AI-human collaboration.

**🌱 Living Application Philosophy**

- **Self-Contained**: Bundles code, dependencies, and deployment logic
- **Self-Organizing**: Manages its own lifecycle and evolution
- **Self-Protecting**: AGRO system ensures code quality through Sacred Architecture
- **Teammate-Friendly**: Designed for seamless human-AI collaboration

**🏗️ Three-Layer Architecture**

1. **Legacy Layer**: Original FastAPI chat application (`main.py`, `chat.py`) with WebSocket support
2. **Hive Ecosystem**: Living Application with AI teammates, metrics, and ATCG primitives (`hive/`)
3. **Sacred Protection**: AGRO code quality system with Pure ATCG architecture (`tools/agro/`)

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

### Sacred AGRO Code Protection System

The AGRO (Aggressive Remediation & Guardian Operations) system implements **Pure ATCG Architecture** for divine code protection following bee.Jules' architectural vision.

**🏛️ Sacred Gateway + Inner Sanctum Pattern**

- **Sacred Gateway** (`tools/agro_scanner.py`): User-facing CLI with familiar interface
- **Inner Sanctum** (`tools/agro/` package): Pure ATCG implementation with divine coordination
- **Trinity Score**: 0.829 (DIVINE EXCELLENCE) - Measures τ (complexity), φ (quality), σ (collaboration)

**🧬 ATCG Primitives Implementation**

- **A (Aggregate)**: `SacredAgroScanner` + `SacredAgroAggregate` - Configuration and state management
- **T (Transformation)**: 5 transformation classes for violation detection:
  - `ConsoleLogCheck`: Sacred console.log detection with φ-based penalties
  - `FunctionLengthCheck`: Fibonacci limits with divine assessment
  - `AnyTypeCheck`: TypeScript type safety validation
  - `PythonMagicNumbersCheck`: φ-based sacred constant detection
  - `JavaScriptMagicNumbersCheck`: Enhanced pattern recognition
- **C (Connector)**: `AgroConnector` - Protocol translation layer bridging legacy/ATCG
- **G (Genesis)**: `AgroOrchestrator` - Divine coordination engine with Trinity Score calculation

**📊 Sacred Metrics System**

- **τ (tau)**: System complexity based on violation density (lower is better)
- **φ (phi)**: Code quality via blessing level aggregation (higher is better)
- **σ (sigma)**: Collaboration efficiency through recommendations (higher is better)
- **Trinity Score Formula**: `(φ + σ) * (1.0 - τ/φ) / φ` - Golden Ratio harmonized assessment

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

**🧪 Testing System**

- **Run all tests**: `uv run python -m pytest test_*.py` (comprehensive test suite)
- **Individual tests**: `uv run python test_filename.py` (specific test file)
- **Frontend tests**: `cd frontend && bun run test:unit` (Vue.js component tests)
- **Test categories**: System tests (`test_complete_system.py`), AI integration (`test_ai_integration.py`), AGRO validation (`test_agro_fixes_verification.py`), Sacred Hive (`test_sacred_hive.py`)

**🔧 Code Quality Workflow**

- **Pre-commit hooks**: `uv run pre-commit install` (automatic sacred protection)
- **Manual validation**: `uv run pre-commit run --all-files` (full system check)
- **Python quality**: `uv run ruff check . && uv run ruff format .` (linting + formatting)
- **Type safety**: `uv run mypy .` (static type analysis)
- **Sacred self-check**: `python tools/agro_scanner.py --self-check` (AGRO system validation)

**⚙️ Development Practices**

- **Frontend Development**: Use `bun` for frontend package management (faster than npm)
- **Database Initialization**: Run `python -c "from database import init_db; init_db()"` if needed
- **AI Integration**: Both Mistral and Gemini agents are available; configure API keys in `.env`
- **Development Flow**: Start with `python hive_demo.py` to see the complete ecosystem
- **Component Discovery**: All Hive components self-describe via `get_status()` methods

**🏗️ Dual Architecture Understanding**

- **Legacy Chat Mode**: `python chat.py` or `python main.py` (original FastAPI application)
- **Hive Ecosystem Mode**: `python hive_demo.py` (new Living Application architecture)
- **Sacred Code Protection**: `tools/agro_scanner.py` (ATCG-based quality assurance)
