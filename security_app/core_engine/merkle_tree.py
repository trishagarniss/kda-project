import hashlib
import os

CHUNK_SIZE = 1024 # memotong ciphertext per 1kb

def sha256_hash(data):
    # untuk hashing data bytes or string
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()

# membentuk merkle tree (fase 3)
def build_merkle_tree(ciphertext_path):
    if not os.path.exists(ciphertext_path):
        raise FileNotFoundError(f"file {ciphertext_path} tidak ditemukan")
    
    level = []
    
    # chunking
    with open(ciphertext_path, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            level.append(sha256_hash(chunk)) # Langsung di-hash dan dimasukkan ke level
            
    if not level:
        return sha256_hash(b"")
    
    # susun bottom up
    while len(level) > 1:
        next_level = []
        for i in range (0, len(level), 2):
            hash1 = level[i]
            hash2 = level[i+1] if i + 1 < len(level) else hash1

            # gabung hash
            combined_hash = sha256_hash(hash1 + hash2)
            next_level.append(combined_hash)
        
        level = next_level
    
    return level[0]

# audit cloud & verif (fase 5)
def verify_data_integrity(ciphertext_path, stored_merkle_root):
    try:
        recalculated_root = build_merkle_tree(ciphertext_path)
    except FileNotFoundError:
        return {
            "is_valid": False,
            "status": "CORRUPTED",
            "message": "Gagal: Ciphertext tidak ditemukan di public cloud"
        }
    
    # pencocokan data
    if recalculated_root == stored_merkle_root:
        return{
            "is_valid": True,
            "status": "Valid",
            "message": "Data identik"
        }
    else:
        return{
            "is_valid": False,
            "status": "CORRUPTED",
            "message": "Data tidak cocok. Ciphertext telah dimodifikasi"
        }