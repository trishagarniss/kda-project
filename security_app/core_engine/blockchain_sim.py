import hashlib
import time
import json
from typing import List, Dict, Any

# BLOCK STRUCTURE
class Block:
    def __init__(self, index: int, file_hash: str, merkle_root: str, prev_hash: str, ciphertext_path: str):
        self.index = index
        self.timestamp = time.time()
        self.file_hash = file_hash
        self.merkle_root = merkle_root
        self.prev_hash = prev_hash
        self.ciphertext_path = ciphertext_path
        self.block_hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "file_hash": self.file_hash,
            "merkle_root": self.merkle_root,
            "prev_hash": self.prev_hash,
            "ciphertext_path": self.ciphertext_path
        }
        data_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "file_hash": self.file_hash,
            "merkle_root": self.merkle_root,
            "prev_hash": self.prev_hash,
            "ciphertext_path": self.ciphertext_path,
            "block_hash": self.block_hash
        }

# BLOCKCHAIN ENGINE
class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(
            index=0,
            file_hash="0" * 64,
            merkle_root="0" * 64,  # Genesis block merkle root
            prev_hash="0" * 64,
            ciphertext_path="genesis_vault"
        )
        self.chain.append(genesis_block)

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, file_hash: str, merkle_root: str, ciphertext_path: str) -> Block:
        prev_block = self.get_last_block()

        new_block = Block(
            index=len(self.chain),
            file_hash=file_hash,
            merkle_root=merkle_root,
            prev_hash=prev_block.block_hash,
            ciphertext_path=ciphertext_path
        )

        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]

            if current.block_hash != current.calculate_hash():
                return False

            if current.prev_hash != prev.block_hash:
                return False

        return True
    
    def find_block_by_hash(self, file_hash):
        for block in self.chain:
            if block.file_hash == file_hash:
                return block
        return None

    def print_chain(self):
        chain_data = [block.to_dict() for block in self.chain]
        print(json.dumps(chain_data, indent=4))