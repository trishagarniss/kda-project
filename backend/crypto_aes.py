import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# HASHING (SHA-256)
def sha256_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_file(filepath: str) -> str:
    with open(filepath, 'rb') as f:
        return sha256_hash(f.read())

# XOR DYNAMIC KEY
def xor_hex(hex1: str, hex2: str) -> bytes:
    """
    XOR dua string hex dan return bytes (32 byte = 256 bit)
    """
    b1 = bytes.fromhex(hex1)
    b2 = bytes.fromhex(hex2)

    # pastikan panjang sama
    length = min(len(b1), len(b2))
    result = bytes([b1[i] ^ b2[i] for i in range(length)])

    return result


def generate_dynamic_key(file_hash: str, prev_hash: str) -> bytes:
    """
    Generate AES-256 key dari XOR hash file dan prev hash
    """
    key = xor_hex(file_hash, prev_hash)

    # pastikan 32 byte (AES-256)
    if len(key) < 32:
        key = key.ljust(32, b'\0')
    else:
        key = key[:32]

    return key


# ENCRYPTION
def encrypt_file(input_path: str, key: bytes, output_path: str):
    """
    Encrypt file menggunakan AES CBC
    """
    with open(input_path, 'rb') as f:
        data = f.read()

    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(pad(data, AES.block_size))

    with open(output_path, 'wb') as f:
        f.write(iv + ciphertext)

    return output_path


# DECRYPTION
def decrypt_file(input_path: str, key: bytes, output_path: str):
    with open(input_path, 'rb') as f:
        file_data = f.read()

    iv = file_data[:16]
    ciphertext = file_data[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    with open(output_path, 'wb') as f:
        f.write(plaintext)

    return output_path


# HASH CIPHERTEXT 
def hash_ciphertext(filepath: str) -> str:
    return hash_file(filepath)