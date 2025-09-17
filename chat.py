import uvicorn
import argparse
import trio_asyncio
from host import app, host
from database import init_db

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000, help="Port to run the web server on")
    parser.add_argument("--p2p-port", type=int, default=4001, help="Port for the P2P node")
    parser.add_argument("--bootstrap-peer", type=str, help="Address of a peer to bootstrap from")
    args = parser.parse_args()

    host.p2p_node.port = args.p2p_port

    init_db()

    # This is a bit of a hack to pass the bootstrap peer to the lifespan context
    # A cleaner solution would be to use a more sophisticated dependency injection system
    async def startup():
        trio_coro = host.p2p_node.start(callback=host.handle_p2p_message, bootstrap_peer=args.bootstrap_peer)
        await trio_asyncio.run_trio_task(trio_coro)
        host.load_default_agents()
        host.logger.info("Hive Host started.")

    app.add_event_handler("startup", startup)

    async def shutdown():
        trio_coro = host.p2p_node.stop()
        await trio_asyncio.run_trio_task(trio_coro)
        host.logger.info("Hive Host shutting down.")

    app.add_event_handler("shutdown", shutdown)

    uvicorn.run(app, host="0.0.0.0", port=args.port)
