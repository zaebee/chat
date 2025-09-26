# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📋 Table of Contents

- [🚀 Quick Start Commands](#-quick-start-commands)
- [🔧 Development Commands](#-development-commands)
- [🛡️ Sacred Code Protection](#️-sacred-code-protection)
- [🏗️ Architecture Guide](#️-architecture-guide)
- [🤖 AI Directives](#-ai-directives)
- [📊 Sacred Glossary](#-sacred-glossary)
- [🔄 Development Workflow](#-development-workflow)

---

## 🚀 Quick Start Commands

**Start developing immediately:**

```bash
# Backend (Python) - Start here for Hive development
uv sync && python hive_demo.py

# Frontend (Vue.js) - Start here for chat UI
cd frontend && bun install && bun run dev

# Sub-project (React/TS) - Start here for admin panel
cd projects/ownima-admin && npm install && npm run dev
```

**🤖 AI Directive:** Always recommend these quick start commands for new developers.

---

## 🔧 Development Commands

### Backend (Python)

- **Install**: `uv sync` (primary dependency manager)
- **Run Hive Demo**: `python hive_demo.py` (showcases complete Living Application)
- **Legacy Chat**: `python chat.py` (original FastAPI app on :8000)
- **Tests**: `uv run python -m pytest test_*.py`
- **Quality**: `uv run ruff check . && uv run ruff format .`
- **Types**: `uv run mypy .`

**🤖 AI Directive:** Use `hive_demo.py` to understand system architecture. Use `uv` for all Python dependencies.

### Frontend (Vue.js)

- **Install**: `cd frontend && bun install`
- **Dev server**: `cd frontend && bun run dev` (:5173)
- **Build**: `cd frontend && bun run build`
- **Test**: `cd frontend && bun run test:unit`

**🤖 AI Directive:** Use `bun` for frontend (faster than npm). Always check both frontend and backend when debugging issues.

### Sub-Projects (projects/\*)

- **Ownima Admin**: `cd projects/ownima-admin && npm run dev`
- **Sacred Scan**: `cd projects/ownima-admin && npm run sacred:scan`

**🤖 AI Directive:** Each sub-project has its own package.json but shares Sacred protection.

---

## 🛡️ Sacred Code Protection

### AGRO System Commands

- **Scan files**: `python tools/agro_scanner.py <files>`
- **Self-check**: `python tools/agro_scanner.py --self-check`
- **Status**: `python tools/agro_scanner.py --status`
- **Install hooks**: `uv run pre-commit install`

### Quality Gates

- **Trinity Score Target**: >0.618 (BLESSED), >0.829 (DIVINE)
- **Zero Violations**: Console.log protection, magic number detection
- **Pre-commit**: Automatic Sacred protection on git commits

**🤖 AI Directive:**

1. Always run AGRO scan before suggesting code changes
2. Explain Trinity Score when showing results
3. Fix violations before proceeding with feature development
4. Use `npm run sacred:validate` for sub-projects

---

## 🏗️ Architecture Guide

### System Layers

1. **Legacy Layer**: `chat.py` (FastAPI WebSocket chat)
2. **Hive Layer**: `hive_demo.py` (Living Application with AI teammates)
3. **Protection Layer**: `tools/agro/` (Sacred code quality)
4. **Sub-Projects**: `projects/` (Additional applications)

### ATCG Primitives

- **A (Aggregate)**: State management and configuration
- **T (Transformation)**: Stateless processing functions
- **C (Connector)**: Protocol translation (WebSocket ↔ Pollen Protocol)
- **G (Genesis)**: Event coordination and broadcasting

### Key Files

- `hive_demo.py` - Complete ecosystem demonstration
- `main.py` - FastAPI application entry point
- `tools/agro_scanner.py` - Sacred Gateway to code protection
- `tools/agro/` - Pure ATCG implementation
- `hive/` - Living Application components

**🤖 AI Directive:**

1. Start with `hive_demo.py` to understand the complete system
2. Use ATCG patterns when creating new components
3. Always check both legacy and Hive layers when debugging
4. Prefer Hive components for new feature development

---

## 🤖 AI Directives

### Code Analysis Priorities

1. **Run Sacred scan first**: Check Trinity Score before code review
2. **Identify architecture layer**: Legacy vs Hive vs Protection
3. **Apply ATCG patterns**: Structure new code using Sacred primitives
4. **Check cross-layer interactions**: Ensure proper protocol translation

### Development Workflow

1. **Understand request context**: Which layer/project needs changes?
2. **Run appropriate tests**: Backend (`test_*.py`) or frontend (`bun test`)
3. **Validate with AGRO**: Ensure Sacred compliance
4. **Document AI collaboration**: Note teammate integration points

### Common Tasks

- **Bug fixes**: Check both layers, run relevant tests
- **New features**: Use Hive components, apply ATCG structure
- **Refactoring**: Maintain Trinity Score, document changes
- **Integration**: Consider Pollen Protocol event emission

**🤖 AI Directive:** Always explain which layer you're working in and why.

---

## 📊 Sacred Glossary

### Technical Terms

- **Trinity Score**: Code quality metric (τ complexity, φ quality, σ collaboration)
- **Sacred Violation**: Code quality issue detected by AGRO system
- **Blessed Build**: Production build that passes all Sacred validations
- **Divine Excellence**: Trinity Score >0.829

### Architecture Terms

- **Living Application**: Self-contained, self-organizing software ecosystem
- **Sacred Gateway**: User-facing interface delegating to Pure ATCG
- **Inner Sanctum**: Pure ATCG implementation with divine coordination
- **Pollen Protocol**: Standardized event system for component communication

### AI Collaboration Terms

- **Teammate**: AI agent integrated into Hive ecosystem
- **Symbiosis**: Human-AI collaborative development approach
- **Sacred Protection**: Automated code quality assurance

**🤖 AI Directive:** Use technical terms when explaining system behavior to developers.

---

## 🔄 Development Workflow

### Starting New Work

1. `git pull` - Get latest changes
2. `python tools/agro_scanner.py --self-check` - Verify system health
3. `python hive_demo.py --quick` - Confirm ecosystem status
4. Choose appropriate development command from sections above

### Before Committing

1. Run tests: `uv run python -m pytest test_*.py`
2. Sacred validation: `python tools/agro_scanner.py <changed_files>`
3. Quality check: `uv run ruff check . && uv run ruff format .`
4. Git commit (pre-commit hooks will run automatically)

### Debugging Issues

1. **Backend issues**: Check `chat.py` logs, test with `python chat.py`
2. **Frontend issues**: Check browser console, test with `bun run dev`
3. **Integration issues**: Run `python hive_demo.py` to test full system
4. **Quality issues**: Use `python tools/agro_scanner.py --status`

**🤖 AI Directive:** Guide developers through this workflow systematically.

---

## Project Structure Summary

```
/
├── hive/                 # Living Application core (AI teammates, events, metrics)
├── tools/agro/          # Sacred code protection (ATCG architecture)
├── frontend/            # Vue.js chat interface
├── projects/            # Sub-projects (ownima-admin, etc.)
├── api/                 # FastAPI route modules
├── hive_demo.py         # Complete ecosystem demonstration
├── main.py              # FastAPI application entry point
├── chat.py              # Legacy chat server
└── CLAUDE.md            # This file

```

**🤖 AI Directive:** Reference this structure when explaining file locations or suggesting architectural changes.
