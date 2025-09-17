import uvicorn
import argparse
from host import app, host

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000, help="Port to run the web server on")
    args = parser.parse_args()

    async def startup():
        await host.lifespan_startup()

    app.add_event_handler("startup", startup)

    async def shutdown():
        await host.lifespan_shutdown()

    app.add_event_handler("shutdown", shutdown)

    uvicorn.run(app, host="0.0.0.0", port=args.port)
