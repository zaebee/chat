import asyncio
from libp2p.host.basic_host import BasicHost
from libp2p.network.swarm import Swarm
from libp2p.peer.peerinfo import PeerInfo
from libp2p.crypto.secp256k1 import create_new_key_pair
from libp2p.pubsub.pubsub import Pubsub
from libp2p.pubsub.gossipsub import GossipSub

class P2PNode:
    def __init__(self, port: int = 4001):
        self.port = port
        self.host = None
        self.pubsub = None

    async def start(self, callback):
        key_pair = create_new_key_pair()
        self.host = BasicHost(key_pair)
        listen_addr = f"/ip4/0.0.0.0/tcp/{self.port}"
        await self.host.get_network().listen(listen_addr)
        self.pubsub = Pubsub(self.host, GossipSub([]))
        print(f"P2P Node started and listening on {listen_addr}")
        print(f"Peer ID: {self.host.get_id().pretty()}")

    async def stop(self):
        if self.host:
            await self.host.close()
            print("P2P Node stopped.")

    async def subscribe(self, topic: str, callback):
        if self.pubsub:
            await self.pubsub.subscribe(topic)
            self.pubsub.subscribe_topic(topic, callback)
            print(f"Subscribed to topic: {topic}")

    async def publish(self, topic: str, message: str):
        if self.pubsub:
            await self.pubsub.publish(topic, message.encode('utf-8'))

    async def get_id(self):
        return self.host.get_id()

    async def get_peers(self):
        return self.host.get_network().connections

    async def get_status(self):
        return {
            "peer_id": self.host.get_id().pretty(),
            "listen_addrs": [str(a) for a in self.host.get_addrs()],
            "peers": len(self.host.get_network().connections)
        }
