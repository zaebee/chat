import trio
from libp2p.p2p_node import P2PNode
import websockets
import asyncio
import argparse

async def p2p_daemon_main(websocket_port: int, p2p_port: int, bootstrap_peer: str = None):
    node = P2PNode(port=p2p_port)
    await node.start(bootstrap_peer=bootstrap_peer) # Starts the trio event loop internally

    async def websocket_handler(websocket, path):
        # Handle messages from the Hive Host
        async for message in websocket:
            # Process message (e.g., publish to libp2p topic)
            # For now, just echo for testing
            print(f"Received from host: {message}")
            await websocket.send(f"Echo: {message}")

    # Start WebSocket server for IPC
    async with websockets.serve(websocket_handler, "localhost", websocket_port):
        print(f"P2P Daemon WebSocket server listening on ws://localhost:{websocket_port}")
        await asyncio.Future() # Run forever

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P2P Daemon for Hive Chat")
    parser.add_argument("--websocket-port", type=int, default=5000, help="Port for WebSocket IPC with Hive Host")
    parser.add_argument("--p2p-port", type=int, default=4001, help="Port for the P2P node")
    parser.add_argument("--bootstrap-peer", type=str, help="Address of a peer to bootstrap from")
    args = parser.parse_args()

    # This daemon runs its own trio event loop
    # We need to run it with `trio.run()`
    trio.run(p2p_daemon_main, args.websocket_port, args.p2p_port, args.bootstrap_peer)
