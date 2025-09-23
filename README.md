# 🐝 Hive Chat: A Living Application Ecosystem

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116%2B-brightgreen)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue)](https://www.typescriptlang.org/)

Welcome to Hive Chat—a revolutionary prototype that demonstrates the future of **"Living Applications"**: self-contained, self-organizing software ecosystems designed for human-AI collaboration.

## 🌿 What is the Hive?

The Hive is more than a chat application. It's a **Living Application** that:

- **Self-Contains**: Bundles code, dependencies, and deployment logic
- **Self-Deploys**: Can deploy as a service, container, or function
- **Self-Organizes**: Manages its own lifecycle and evolution
- **Collaborates**: Designed for seamless human-AI teamwork

## 📋 Current Status: Phase 1 Chat Enhancements

**Latest Update**: Phase 1 frontend enhancements are now available! 🎉

- ✅ **Rich Text & Markdown Support**: Real-time markdown rendering with syntax highlighting
- ✅ **Enhanced Chat Experience**: Improved input, reactions, and typing indicators  
- ✅ **Production Ready**: All features work without backend changes
- 📖 **[Phase 1 Documentation](./PHASE1_README.md)**: Complete implementation guide

> **Note**: Phase 1 focuses on frontend-only improvements for immediate value. Backend integration and real-time multi-user features are planned for Phase 2.

## 🚀 Quick Start

### Option 1: Try the Demo (2 minutes)
```bash
git clone https://github.com/zaebee/chat.git
cd chat
python hive_demo.py --quick
```

### Option 2: Full Development Setup (10 minutes)
```bash
# Backend setup
uv sync
python -c "from database import init_db; init_db()"

# Frontend setup  
cd frontend && bun install && bun run dev

# Start the Hive ecosystem
python hive_demo.py
```

### Option 3: Simple Chat Mode
```bash
python chat.py
# Open http://localhost:8000
```

## 🧬 Architecture: The ATCG Primitives

The Hive is built on four fundamental "genetic" components:

- **A**ggregates → Structure and state management
- **T**ransformations → Processing and business logic  
- **C**onnectors → Communication and interfaces
- **G**enesis Events → Memory and system evolution

## 🤖 AI Teammates

The Hive includes integrated AI agents:

- **Mistral Agent** - Code analysis and generation
- **Gemini Agent** - Multi-modal understanding and reasoning
- **Extensible Framework** - Add your own AI teammates

## 🎓 Learning Platform

Built-in Python learning environment with:

- **Interactive Challenges** - Hands-on coding exercises
- **Pyodide Integration** - Python runtime in the browser
- **Gamification** - XP, badges, and progression tracking
- **Collaborative Learning** - Human-AI pair programming

## Documentation

All detailed documentation, including our vision, architectural principles, roadmap, and technical requirements, can be found in the `docs/` directory.

Comprehensive documentation organized by audience:

- **[📖 Complete Documentation Index](docs/README.md)** - Start here
- **[🚀 Getting Started Guide](docs/02_DEVELOPMENT/GETTING_STARTED.md)** - Developer setup
- **[🌟 Vision & Philosophy](docs/00_FOUNDATION/VISION.md)** - The big picture
- **[🏗️ Architecture Guide](docs/01_ARCHITECTURE/OVERVIEW.md)** - System design
- **[🎯 User Guides](docs/04_USER_GUIDES/)** - For students and educators

## 🛠️ Tech Stack

### Backend
- **Python 3.10+** with FastAPI
- **SQLite** database with automatic initialization
- **WebSocket** real-time communication
- **Mistral AI & Google Gemini** integration
- **Event-driven architecture** with Pollen Protocol

### Frontend  
- **Vue.js 3** with TypeScript
- **Vite** build system
- **Pinia** state management
- **CodeMirror** in-browser code editor
- **Pyodide** Python runtime in WebAssembly

## ✨ Phase 1 Features (Available Now)

### 🎨 Rich Text & Markdown Support
- **Live Markdown Preview**: Real-time rendering with syntax highlighting
- **Formatting Toolbar**: Rich text controls (bold, italic, code, lists)
- **Formatting Help**: Comprehensive markdown guide and assistance
- **Enhanced Renderer**: Improved markdown composable with extended features

### 💬 Enhanced Chat Experience
- **Improved Chat Input**: Better UX with formatting integration and auto-resize
- **Message Reactions**: Local emoji reaction system with immediate feedback
- **Typing Indicators**: Real-time typing status with WebSocket integration
- **Better Message Display**: Cleaner layout and improved interaction patterns

### 🔧 Technical Improvements
- **Production Build**: Optimized TypeScript and Vite configuration
- **Type Safety**: Enhanced TypeScript types and build exclusions
- **Development Experience**: Improved tooling and error handling
- **Graceful Degradation**: Features work offline with local fallbacks

> **📖 [Complete Phase 1 Documentation](./PHASE1_README.md)** - Implementation details, limitations, and migration path

## 🌱 Philosophy: Human-AI Symbiosis

The Hive embodies five core principles:

1. **Legibility** - All components are self-describing
2. **Observability** - The system announces its state continuously  
3. **Modularity** - Composable, loosely-coupled architecture
4. **API-First** - Everything accessible programmatically
5. **Symbiosis** - Designed for human-AI collaboration

## 🎯 Use Cases

- **Educational Platform** - Interactive Python learning
- **AI Development** - Framework for AI agent collaboration
- **Research Tool** - Study human-AI interaction patterns
- **Prototype Platform** - Test "Living Application" concepts
- **Community Hub** - Collaborative coding and learning

## 🤝 Contributing

We welcome contributions from both humans and AI agents:

1. **Read the [Contributing Guide](docs/02_DEVELOPMENT/CONTRIBUTING.md)**
2. **Explore the [Architecture Docs](docs/01_ARCHITECTURE/)**
3. **Check [Open Issues](https://github.com/zaebee/chat/issues)**
4. **Join the Discussion** in our chat platform

## 📊 System Health

The Hive monitors three key metrics:

- **τ (Tau)** - System complexity (lower is better)
- **φ (Phi)** - Code quality (higher is better)  
- **σ (Sigma)** - Collaborative efficiency

## 🔮 Future Vision

The Hive is a stepping stone toward:

- **Autonomous Software** that can reproduce and evolve
- **Decentralized Applications** that don't depend on central authorities
- **AI-Native Development** where AI agents are first-class citizens
- **Living Code** that grows and adapts like biological systems

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Join the Hive

Ready to explore the future of software? 

**[Start with our Getting Started Guide →](docs/02_DEVELOPMENT/GETTING_STARTED.md)**

---

*"In the Hive, we don't just write code—we cultivate life."* 🐝✨
*   [**Start Here: The Hive Vision**](docs/00_VISION.md)
*   [**Project Roadmap**](docs/02_ROADMAP.md)
*   [**Technical Requirements**](docs/03_REQUIREMENTS.md)
*   [**Our Team & Consultations**](docs/team/index.md)

## Getting Started

# Hive Chat

Welcome to Hive Chat, a project exploring the future of decentralized, self-organizing applications.

This project is a prototype of a **"Living Application"** – a single, self-contained binary that can deploy itself, manage its own lifecycle, and host other intelligent agents.

## Documentation

All detailed documentation, including our vision, architectural principles, roadmap, and technical requirements, can be found in the `docs/` directory.

*   [**Start Here: The Hive Vision**](docs/00_VISION.md)
*   [**Project Roadmap**](docs/02_ROADMAP.md)
*   [**Technical Requirements**](docs/03_REQUIREMENTS.md)
*   [**Our Team & Consultations**](docs/team/index.md)

## Getting Started

Instructions on how to set up the development environment and run the application will be provided in the documentation.
>>>>>>> main
