import trio
from libp2p import new_node
import websockets
import asyncio
import argparse
from multiaddr import Multiaddr

async def p2p_daemon_main(websocket_port: int, p2p_port: int, bootstrap_peer: str = None):
    node = await new_node(transport_opt=[f"/ip4/0.0.0.0/tcp/{p2p_port}"])
    await node.get_network().listen(f"/ip4/0.0.0.0/tcp/{p2p_port}")
    print(f"P2P Node started with Peer ID: {node.get_id().pretty()}")

    if bootstrap_peer:
        bootstrap_addr = Multiaddr(bootstrap_peer)
        await node.get_network().connect(bootstrap_addr)
        print(f"Connected to bootstrap peer: {bootstrap_peer}")

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
        print("P2P_DAEMON_READY")
        try:
            await asyncio.Future() # Run forever
        finally:
            await node.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P2P Daemon for Hive Chat")
    parser.add_argument("--websocket-port", type=int, default=5000, help="Port for WebSocket IPC with Hive Host")
    parser.add_argument("--p2p-port", type=int, default=4001, help="Port for the P2P node")
    parser.add_argument("--bootstrap-peer", type=str, help="Address of a peer to bootstrap from")
    args = parser.parse_args()

    # This daemon runs its own trio event loop
    # We need to run it with `trio.run()`
    trio.run(p2p_daemon_main, args.websocket_port, args.p2p_port, args.bootstrap_peer)
