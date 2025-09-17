import asyncio
import logging
import sys
from fastapi import FastAPI
import websockets
from agents.chat_agent import ChatAgent # Import ChatAgent

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
        formatter = logging.Formatter('{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "agent": "%(name)s"}')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    async def lifespan_startup(self):
        self.logger.info("Hive Host starting.")
        websocket_port = 5000 # Fixed port for p2p daemon IPC

        # Start the P2P Daemon process
        self.p2p_daemon_process = await asyncio.create_subprocess_exec(
            sys.executable, "p2p_daemon.py",
            "--websocket-port", str(websocket_port),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        self.logger.info(f"P2P Daemon started with PID: {self.p2p_daemon_process.pid}")

        # Start a task to read stderr from the daemon
        asyncio.create_task(self._read_daemon_stderr())

        # Start the event consumer task
        asyncio.create_task(self._event_consumer())

        # Wait for daemon to signal readiness
        while True:
            line = await self.p2p_daemon_process.stdout.readline()
            if line.strip() == b"P2P_DAEMON_READY":
                self.logger.info("P2P Daemon is ready.")
                break

        # Connect to the P2P Daemon via WebSocket
        self.p2p_websocket_client = await websockets.connect(f"ws://localhost:{websocket_port}")
        self.logger.info("Connected to P2P Daemon WebSocket.")

        await self.load_default_agents()
        self.logger.info("Hive Host started.")

    async def _event_consumer(self):
        while True:
            event = await self.event_bus.get()
            self.logger.info(f"Event received: {event}")

    async def lifespan_shutdown(self):
        self.logger.info("Hive Host shutting down.")
        if self.p2p_websocket_client:
            await self.p2p_websocket_client.close()
        if self.p2p_daemon_process:
            self.p2p_daemon_process.terminate()
            await self.p2p_daemon_process.wait()

    async def load_default_agents(self):
        # Agents receive the host's core services and a way to talk to the p2p daemon
        chat_agent = ChatAgent(self.p2p_websocket_client, self.event_bus, self.logger, self.fastapi_app)
        self.agents.append(chat_agent)
        await chat_agent.start()
        self.logger.info(f"Loaded agent: {chat_agent.get_status()['name']}")

    async def handle_p2p_message(self, msg):
        # This method will be called by the p2p daemon via WebSocket
        # For now, just put it on the event bus
        await self.event_bus.put(msg)

    async def _read_daemon_stderr(self):
        while True:
            line = await self.p2p_daemon_process.stderr.readline()
            if line:
                self.logger.error(f"P2P Daemon STDERR: {line.decode().strip()}")
            else:
                break

    def setup_api_routes(self):
        @self.fastapi_app.get("/api/v1/status")
        async def get_system_status():
            # Query daemon for p2p status
            await self.p2p_websocket_client.send(json.dumps({"command": "get_status"}))
            daemon_status = json.loads(await self.p2p_websocket_client.recv())
            return {
                "status": "running",
                "p2p_daemon": daemon_status,
                "agents": [agent.get_status() for agent in self.agents]
            }

host = HiveHost()
app = host.fastapi_app