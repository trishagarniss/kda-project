import os
import time
import hashlib

def benchmark_hashing(filepath):
    if not os.path.exists(filepath):
        print(f"File {filepath} tidak ditemukan. Membuat file dummy 50MB...")
        # Buat file dummy 50MB
        filepath = "dummy_benchmark.bin"
        with open(filepath, "wb") as f:
            f.write(os.urandom(50 * 1024 * 1024))
            
    file_size = os.path.getsize(filepath)
    file_size_mb = file_size / (1024 * 1024)
    print(f"=== BENCHMARK HASHING ===")
    print(f"Ukuran File: {file_size_mb:.2f} MB")
    print("-" * 40)

    # 1. Benchmark SHA-256
    start_time = time.time()
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    hash_sha256 = sha256.hexdigest()
    elapsed_sha256 = time.time() - start_time
    speed_sha256 = file_size_mb / elapsed_sha256

    print(f"SHA-2 (SHA-256):")
    print(f"  - Hash  : {hash_sha256}")
    print(f"  - Waktu : {elapsed_sha256:.4f} detik")
    print(f"  - Speed : {speed_sha256:.2f} MB/s")
    print("-" * 40)

    # 2. Benchmark SHA-3-256 (Keccak-256)
    start_time = time.time()
    sha3_256 = hashlib.sha3_256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            sha3_256.update(chunk)
    hash_sha3 = sha3_256.hexdigest()
    elapsed_sha3 = time.time() - start_time
    speed_sha3 = file_size_mb / elapsed_sha3

    print(f"SHA-3 (Keccak-256):")
    print(f"  - Hash  : {hash_sha3}")
    print(f"  - Waktu : {elapsed_sha3:.4f} detik")
    print(f"  - Speed : {speed_sha3:.2f} MB/s")
    print("-" * 40)

    # Bersihkan file dummy jika dibuat otomatis
    if filepath == "dummy_benchmark.bin" and os.path.exists("dummy_benchmark.bin"):
        os.remove("dummy_benchmark.bin")

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else ""
    benchmark_hashing(path)
