import hashlib
import time
import json


# BLOCK STRUCTURE
class Block:
    def __init__(self, index, file_hash, merkle_root, prev_hash, ciphertext_path):
        self.index = index
        self.timestamp = time.time()
        self.file_hash = file_hash
        self.merkle_root = merkle_root
        self.prev_hash = prev_hash
        self.ciphertext_path = ciphertext_path
        self.block_hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.timestamp}{self.file_hash}{self.merkle_root}{self.prev_hash}{self.ciphertext_path}"
        return hashlib.sha256(data.encode()).hexdigest()

    def to_dict(self):
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
        self.chain = []
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

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, file_hash, merkle_root, ciphertext_path):
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