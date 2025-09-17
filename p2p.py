import asyncio
from libp2p.host.basic_host import BasicHost
from libp2p.network.swarm import Swarm
from libp2p.peer.id import ID as PeerID
from libp2p.peer.peerstore import PeerStore
from libp2p.crypto.secp256k1 import create_new_key_pair
from libp2p.pubsub.pubsub import Pubsub
from libp2p.pubsub.gossipsub import GossipSub
from libp2p.transport.tcp.tcp import TCP
from libp2p.transport.upgrader import TransportUpgrader
from libp2p.stream_muxer.mplex.mplex import Mplex
from libp2p.security.noise.transport import Noise
from multiaddr import Multiaddr

class P2PNode:
    def __init__(self, port: int = 4001):
        self.port = port
        self.host = None
        self.pubsub = None

    async def start(self, callback, bootstrap_peer: str = None):
        key_pair = create_new_key_pair()
        peer_id = PeerID.from_pubkey(key_pair.public_key)
        
        peerstore = PeerStore()
        peerstore.add_key_pair(peer_id, key_pair)

        upgrader = TransportUpgrader(Noise(key_pair), Mplex())
        transport = TCP()
        
        swarm = Swarm(peer_id, peerstore, upgrader, transport)
        self.host = BasicHost(swarm)
        
        listen_addr = f"/ip4/0.0.0.0/tcp/{self.port}"
        await self.host.get_network().listen(listen_addr)
        self.pubsub = Pubsub(self.host, GossipSub([]))
        print(f"P2P Node started and listening on {listen_addr}")
        print(f"Peer ID: {self.host.get_id().pretty()}")

        if bootstrap_peer:
            bootstrap_addr = Multiaddr(bootstrap_peer)
            await self.host.connect(bootstrap_addr)
            print(f"Connected to bootstrap peer: {bootstrap_peer}")

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
        if not self.host:
            return {"status": "stopped"}
        return {
            "peer_id": self.host.get_id().pretty(),
            "listen_addrs": [str(a) for a in self.host.get_addrs()],
            "peers": len(self.host.get_network().connections)
        }
