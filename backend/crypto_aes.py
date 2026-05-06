import hashlib
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# HASHING (SHA-256)
def sha256_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def hash_file(filepath: str) -> str:
    with open(filepath, 'rb') as f:
        return sha256_hash(f.read())

# DYNAMIC KEY GENERATION (XOR)
def xor_hex(hex1: str, hex2: str) -> bytes:
    # XOR dua string hex dan return bytes (32 byte = 256 bit)
    b1 = bytes.fromhex(hex1)
    b2 = bytes.fromhex(hex2)

    length = min(len(b1), len(b2))
    result = bytes([b1[i] ^ b2[i] for i in range(length)])

    return result

def generate_dynamic_key(file_hash: str, prev_hash: str) -> bytes:
    # Generate AES-256 key dari XOR hash file dan prev hash
    key = xor_hex(file_hash, prev_hash)

    # pastikan 32 byte (AES-256)
    if len(key) < 32:
        key = key.ljust(32, b'\0')
    else:
        key = key[:32]

    return key

# ENCRYPTION (AES-256-GCM)
def encrypt_file(input_path: str, key: bytes, output_path: str):
    # Encrypt file menggunakan AES-256-GCM sesuai arsitektur CloudGuard EMT.
    with open(input_path, 'rb') as f:
        data = f.read()

    aesgcm = AESGCM(key)
    
    nonce = os.urandom(12)
    
    ciphertext = aesgcm.encrypt(nonce, data, None)

    with open(output_path, 'wb') as f:
        f.write(nonce + ciphertext)

    return output_path

# DECRYPTION (AES-256-GCM)
def decrypt_file(input_path: str, key: bytes, output_path: str):
    with open(input_path, 'rb') as f:
        file_data = f.read()

    # Pisahkan 12 byte pertama sebagai Nonce, sisanya adalah Ciphertext + Tag
    nonce = file_data[:12]
    ciphertext = file_data[12:]

    aesgcm = AESGCM(key)
    
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    with open(output_path, 'wb') as f:
        f.write(plaintext)

    return output_path


# HASH CIPHERTEXT 
def hash_ciphertext(filepath: str) -> str:
    return hash_file(filepath)