# 🐝 Hive Chat - A Collaborative Learning Environment

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-brightgreen)](https://fastapi.tiangolo.com/)

This project is a **"Living Application"**—a collaborative chat environment designed for students learning to code. It combines a real-time chat application with an interactive Python playground, allowing students to solve coding challenges and get immediate feedback, all within the browser.

Our goal is to create a resilient, peer-to-peer communication system that is not just a tool, but a habitat for human and AI teammates to collaborate and learn together.

## 📚 Documentation

All detailed documentation regarding our vision, architecture, roadmap, and requirements can be found in the `/docs` directory.

*   **[Start Here: Project Vision](./docs/00_VISION.md)**
*   **[Architectural Principles](./docs/01_ARCHITECTURE.md)**
*   **[Modern UI PRD](./docs/04_CHAT_MODERN_UI_PRD.md)**
*   **[Python Learning Module FRD](./docs/05_PYTHON_LEARNING_MODULE_FRD.md)**

## 🏃‍♀️ Getting Started

This project consists of a Python/FastAPI backend and a Vue.js frontend. You will need to run both simultaneously.

### 1. Backend (Python)

The backend handles WebSocket connections, message broadcasting, and data persistence.

```bash
# Install Python dependencies
# (uv is recommended)
uv sync

# Run the backend server
python chat.py
```

The backend will run on `http://localhost:8000`.

### 2. Frontend (Vue.js)

The frontend is a modern single-page application built with Vue.js and Vite.

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies (bun is recommended)
bun install

# Run the frontend development server
bun run dev
```

The frontend will be available at `http://localhost:5173` (or the next available port).

## 🤝 Contributing

We welcome all contributors, human or AI. Please see our [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.