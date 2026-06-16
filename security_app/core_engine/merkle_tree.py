import hashlib
import os

CHUNK_SIZE = 1024 # memotong ciphertext per 1kb

def hash_data(data, algo="SHA256"):
    # untuk hashing data bytes or string
    if isinstance(data, str):
        data = data.encode()
    if algo == "SHA3_256":
        return hashlib.sha3_256(data).hexdigest()
    return hashlib.sha256(data).hexdigest()

# membentuk merkle tree (fase 3)
def build_merkle_tree(ciphertext_path, algo="SHA256"):
    if not os.path.exists(ciphertext_path):
        raise FileNotFoundError(f"file {ciphertext_path} tidak ditemukan")
    
    level = []
    
    # chunking
    with open(ciphertext_path, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            level.append(hash_data(chunk, algo)) # Hashing dengan algo terpilih
            
    if not level:
        return hash_data(b"", algo)
    
    # susun bottom up
    while len(level) > 1:
        next_level = []
        for i in range (0, len(level), 2):
            hash1 = level[i]
            hash2 = level[i+1] if i + 1 < len(level) else hash1

            # gabung hash
            combined_hash = hash_data(hash1 + hash2, algo)
            next_level.append(combined_hash)
        
        level = next_level
    
    return level[0]

# audit cloud & verif (fase 5)
def verify_data_integrity(ciphertext_path, stored_merkle_root, algo="SHA256"):
    try:
        recalculated_root = build_merkle_tree(ciphertext_path, algo)
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