import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

CHUNK_SIZE = 65536 # 64KB

# HASHING (SHA-256)
def sha256_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def hash_file(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} tidak ditemukan.")
        
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()

# DYNAMIC KEY GENERATION (XOR)
def xor_hex(hex1: str, hex2: str) -> bytes:
    # XOR dua string hex dan return bytes (32 byte = 256 bit)
    b1 = bytes.fromhex(hex1)
    b2 = bytes.fromhex(hex2)
    return bytes(a ^ b for a, b in zip(b1, b2))

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
def encrypt_file(input_path: str, key: bytes, output_path: str) -> str:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File {input_path} tidak ditemukan.")

    nonce = os.urandom(12)
    encryptor = Cipher(algorithms.AES(key), modes.GCM(nonce)).encryptor()

    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        f_out.write(nonce)
        
        while chunk := f_in.read(CHUNK_SIZE):
            f_out.write(encryptor.update(chunk))
            
        encryptor.finalize()
        f_out.write(encryptor.tag)

    return output_path

# DECRYPTION (AES-256-GCM)
def decrypt_file(input_path: str, key: bytes, output_path: str) -> str:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File {input_path} tidak ditemukan.")

    file_size = os.path.getsize(input_path)
    if file_size < 28:
        raise ValueError("File corrupted: Terlalu kecil untuk AES-GCM.")

    with open(input_path, 'rb') as f_in:
        nonce = f_in.read(12)
        
        f_in.seek(-16, os.SEEK_END)
        tag = f_in.read(16)
        
        f_in.seek(12)
        decryptor = Cipher(algorithms.AES(key), modes.GCM(nonce, tag)).decryptor()
        
        with open(output_path, 'wb') as f_out:
            bytes_to_read = file_size - 28
            while bytes_to_read > 0:
                chunk = f_in.read(min(CHUNK_SIZE, bytes_to_read))
                if not chunk: break
                f_out.write(decryptor.update(chunk))
                bytes_to_read -= len(chunk)
                
            decryptor.finalize() 

    return output_path


# HASH CIPHERTEXT 
def hash_ciphertext(filepath: str) -> str:
    return hash_file(filepath)