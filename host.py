import asyncio
import logging
from fastapi import FastAPI
import websockets
from agents.chat_agent import ChatAgent

class HiveHost:
    def __init__(self):
        self.p2p_daemon_process = None
        self.p2p_websocket_client = None
        self.event_bus = asyncio.Queue()
        self.logger = self.setup_logger()
        self.fastapi_app = FastAPI()
        self.setup_api_routes()

    def setup_logger(self):
        logger = logging.getLogger("hive")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    async def lifespan_startup(self, p2p_port: int, bootstrap_peer: str = None):
        self.logger.info("Hive Host starting.")
        websocket_port = 5000 # Fixed port for p2p daemon IPC

        # Start the P2P Daemon process
        self.p2p_daemon_process = await asyncio.create_subprocess_exec(
            "python", "p2p_daemon.py",
            "--websocket-port", str(websocket_port),
            "--p2p-port", str(p2p_port),
            *(("--bootstrap-peer", bootstrap_peer) if bootstrap_peer else ()),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        self.logger.info(f"P2P Daemon started with PID: {self.p2p_daemon_process.pid}")

        # Wait for daemon to signal readiness
        while True:
            line = await self.p2p_daemon_process.stdout.readline()
            if line.strip() == b"P2P_DAEMON_READY":
                self.logger.info("P2P Daemon is ready.")
                break

        # Connect to the P2P Daemon via WebSocket
        self.p2p_websocket_client = await websockets.connect(f"ws://localhost:{websocket_port}")
        self.logger.info("Connected to P2P Daemon WebSocket.")

        self.load_default_agents()
        self.logger.info("Hive Host started.")

    async def lifespan_shutdown(self):
        self.logger.info("Hive Host shutting down.")
        if self.p2p_websocket_client:
            await self.p2p_websocket_client.close()
        if self.p2p_daemon_process:
            self.p2p_daemon_process.terminate()
            await self.p2p_daemon_process.wait()

    def load_default_agents(self):
        # Agents receive the host's core services and a way to talk to the p2p daemon
        chat_agent = ChatAgent(self.p2p_websocket_client, self.event_bus, self.logger, self.fastapi_app)
        self.agents.append(chat_agent)
        chat_agent.start()
        self.logger.info(f"Loaded agent: {chat_agent.get_status()['name']}")

    async def handle_p2p_message(self, msg):
        # This method will be called by the p2p daemon via WebSocket
        # For now, just put it on the event bus
        await self.event_bus.put(msg)

    def setup_api_routes(self):
        @self.fastapi_app.get("/api/v1/status")
        async def get_system_status():
            # Query daemon for p2p status
            await self.p2p_websocket_client.send("get_status")
            daemon_status = await self.p2p_websocket_client.recv()
            return {
                "status": "running",
                "p2p_daemon": daemon_status,
                "agents": [agent.get_status() for agent in self.agents]
            }

host = HiveHost()
app = host.fastapi_app
