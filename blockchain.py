import hashlib
import json
import time
from dataclasses import dataclass, asdict
from typing import List


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


@dataclass
class Block:
    index: int
    timestamp: float
    data: dict
    prev_hash: str
    nonce: int
    hash: str


class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.chain: List[Block] = [self._create_genesis_block()]

    def _create_genesis_block(self) -> Block:
        genesis = Block(
            index=0,
            timestamp=time.time(),
            data={"msg": "genesis"},
            prev_hash="0" * 64,
            nonce=0,
            hash=""
        )
        mined = self._mine_block(genesis)
        return mined

    def _block_payload(self, block: Block) -> str:
        payload = {
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "prev_hash": block.prev_hash,
            "nonce": block.nonce,
        }
        return json.dumps(payload, sort_keys=True)

    def _mine_block(self, block: Block) -> Block:
        target_prefix = "0" * self.difficulty
        nonce = 0
        while True:
            block.nonce = nonce
            h = sha256(self._block_payload(block))
            if h.startswith(target_prefix):
                block.hash = h
                return block
            nonce += 1

    def add_block(self, data: dict) -> Block:
        prev = self.chain[-1]
        new_block = Block(
            index=prev.index + 1,
            timestamp=time.time(),
            data=data,
            prev_hash=prev.hash,
            nonce=0,
            hash=""
        )
        mined = self._mine_block(new_block)
        self.chain.append(mined)
        return mined

    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.prev_hash != prev.hash:
                return False
            if sha256(self._block_payload(curr)) != curr.hash:
                return False
            if not curr.hash.startswith("0" * self.difficulty):
                return False
        return True

    def to_list(self):
        return [asdict(b) for b in self.chain]
