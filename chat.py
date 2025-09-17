import uvicorn
import argparse
from host import app, host

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000, help="Port to run the web server on")
    parser.add_argument("--p2p-port", type=int, default=4001, help="Port for the P2P node")
    parser.add_argument("--bootstrap-peer", type=str, help="Address of a peer to bootstrap from")
    args = parser.parse_args()

    async def startup():
        await host.lifespan_startup(p2p_port=args.p2p_port, bootstrap_peer=args.bootstrap_peer)

    app.add_event_handler("startup", startup)

    async def shutdown():
        await host.lifespan_shutdown()

    app.add_event_handler("shutdown", shutdown)

    uvicorn.run(app, host="0.0.0.0", port=args.port)
