import asyncio
import websockets
import argparse
import json

async def mock_p2p_daemon_main(websocket_port: int):
    async def websocket_handler(websocket, path):
        print(f"Mock P2P Daemon: WebSocket connection established with {path}")
        try:
            async for message in websocket:
                print(f"Mock P2P Daemon: Received from host: {message}")
                # Simulate processing and sending a response
                response = {"status": "mock_response", "received_message": message}
                if message == "get_status":
                    response = {"status": "mock_running", "peer_id": "mock_peer_id", "peers": 0}
                await websocket.send(json.dumps(response))
        except websockets.exceptions.ConnectionClosedOK:
            print("Mock P2P Daemon: WebSocket connection closed.")
        except Exception as e:
            print(f"Mock P2P Daemon: Error in websocket_handler: {e}")

    # Start WebSocket server for IPC
    async with websockets.serve(websocket_handler, "localhost", websocket_port):
        print(f"Mock P2P Daemon WebSocket server listening on ws://localhost:{websocket_port}")
        print("P2P_DAEMON_READY") # Signal readiness to the host
        await asyncio.Future() # Run forever

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mock P2P Daemon for Hive Chat")
    parser.add_argument("--websocket-port", type=int, default=5000, help="Port for WebSocket IPC with Hive Host")
    # We don't need p2p-port or bootstrap-peer for the mock daemon
    args = parser.parse_args()

    asyncio.run(mock_p2p_daemon_main(args.websocket_port))
