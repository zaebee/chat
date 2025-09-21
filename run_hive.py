import uvicorn
import argparse

# This script now has a single, sacred purpose: to run the app from main.py

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sacred Hive Launcher")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    args = parser.parse_args()

    print(f"🐝 Starting Sacred Hive on {args.host}:{args.port}")
    # We point uvicorn directly to the 'app' object inside the 'main' module.
    uvicorn.run("main:app", host=args.host, port=args.port, reload=args.reload)
