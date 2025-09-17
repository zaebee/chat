import asyncio
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
# from libp2p.p2p_node import P2PNode  # Hypothetical import
from agents.chat_agent import ChatAgent

class HiveHost:
    def __init__(self):
        # self.p2p_node = P2PNode()
        self.agents = []
        self.event_bus = asyncio.Queue()
        self.logger = self.setup_logger()
        self.fastapi_app = FastAPI(lifespan=self.lifespan)
        self.setup_api_routes()

    def setup_logger(self):
        logger = logging.getLogger("hive")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        # On startup
        # await self.p2p_node.start()
        self.load_default_agents()
        self.logger.info("Hive Host started.")
        yield
        # On shutdown
        self.logger.info("Hive Host shutting down.")
        # await self.p2p_node.stop()

    def load_default_agents(self):
        # chat_agent = ChatAgent(self.p2p_node, self.event_bus, self.logger, self.fastapi_app)
        chat_agent = ChatAgent(self.event_bus, self.logger, self.fastapi_app)
        self.agents.append(chat_agent)
        chat_agent.start()
        self.logger.info(f"Loaded agent: {chat_agent.get_status()['name']}")

    def setup_api_routes(self):
        @self.fastapi_app.get("/api/v1/status")
        async def get_system_status():
            return {
                "status": "running",
                "agents": [agent.get_status() for agent in self.agents]
            }

host = HiveHost()
app = host.fastapi_app
