# GEMINI.md

## Project Overview

This project is a multi-user chat application built with Python and FastAPI. It uses WebSockets for real-time communication between users. The frontend is a single HTML page rendered with Jinja2, and it uses vanilla JavaScript to handle the WebSocket connection and UI updates.

The main technologies used are:

*   **Backend:** Python, FastAPI, Uvicorn
*   **Frontend:** HTML, CSS, JavaScript
*   **Real-time:** WebSockets
*   **Templating:** Jinja2

The application supports multiple users, message history, user join/leave notifications, and color-coded user names.

## Building and Running

To run the application, you need to have Python and `uv` installed.

1.  **Install dependencies:**

    ```bash
    uv sync
    ```

2.  **Run the application:**

    ```bash
    uv run chat.py
    ```

    Or, more explicitly with uvicorn:

    ```bash
    uvicorn chat:app --host 0.0.0.0 --port 8000
    ```

The application will be available at `http://localhost:8000`.

## Development Conventions

*   The main application logic is contained in a single file, `chat.py`.
*   The frontend is a single HTML file, `templates/chat.html`, which includes inline CSS and JavaScript.
*   The application state (users, messages) is stored in memory in the `ConnectionManager` class.
*   The project uses `pyproject.toml` to manage dependencies.
