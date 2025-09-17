# Contributing to Hive Chat

First off, thank you for considering contributing to Hive Chat! It's people like you that make the open-source community such a great place.

## Getting Started

### System-Level Prerequisites

Before setting up the Python environment, please ensure you have the following system-level dependencies installed:

```bash
# For Debian-based systems (like Ubuntu)
sudo apt-get update
sudo apt-get install libgmp-dev
```

### Python Environment

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** to your local machine:
    ```bash
    git clone https://github.com/YOUR_USERNAME/chat.git
    ```
3.  **Set up the development environment:**
    ```bash
    uv sync
    ```

## Making Changes

1.  **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/your-amazing-feature
    ```
2.  **Make your changes** and ensure the code follows the existing style.
3.  **Run the application** to test your changes locally:
    ```bash
    uv run chat.py
    ```

## Submitting Your Changes

1.  **Commit your changes** with a clear and descriptive commit message:
    ```bash
    git commit -m "feat: Add some amazing feature"
    ```
2.  **Push your changes** to your fork on GitHub:
    ```bash
    git push origin feature/your-amazing-feature
    ```
3.  **Open a pull request** from your fork to the main Hive Chat repository.

## Coding Style

*   Please follow the existing code style.
*   We use `black` for code formatting. Before you commit, please run `black .` to format your code.
*   Write clear and concise comments where necessary.

Thank you for your contributions!
