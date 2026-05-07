import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SecureDocument

# Import mesin kriptografi kalian dari folder core_engine
from .core_engine.crypto_aes import encrypt_file, hash_file, generate_dynamic_key
from .core_engine.blockchain_sim import Blockchain
from .core_engine.merkle_tree import build_merkle_tree

# Inisialisasi Blockchain CloudGuard
cloudguard_chain = Blockchain()

@csrf_exempt
def upload_and_secure(request):
    if request.method == 'POST' and request.FILES.get('document'):
        uploaded_file = request.FILES['document']
        file_name = uploaded_file.name
        file_size = uploaded_file.size
        
        # 1. Simpan sementara
        temp_path = f"temp_{file_name}"
        with open(temp_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
                
        # 2. Proses Kriptografi 
        file_hash = hash_file(temp_path)
        prev_hash = cloudguard_chain.get_last_block().block_hash
        key = generate_dynamic_key(file_hash, prev_hash)
        
        os.makedirs("media/encrypted_vault", exist_ok=True)
        encrypted_path = f"media/encrypted_vault/{file_name}.bin"
        encrypt_file(temp_path, key, encrypted_path)
        
        # 3. Hitung Merkle Root Asli
        merkle_root = build_merkle_tree(encrypted_path)
        
        # 4. Catat ke Blockchain
        new_block = cloudguard_chain.add_block(file_hash, merkle_root, encrypted_path)
        
        # 5. Simpan ke Supabase (Merespon: Tambah field baru)
        doc_record = SecureDocument.objects.create(
            file_name=file_name,
            file_size=file_size,
            file_hash=new_block.file_hash,
            merkle_root=new_block.merkle_root,
            block_index=new_block.index,
            prev_hash=new_block.prev_hash,
            ciphertext_path=new_block.ciphertext_path,
            status_verifikasi="VALID" 
        )
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return JsonResponse({
            "status": "Sukses",
            "message": "File berhasil diamankan oleh CloudGuard EMT!",
            "data": {
                "database_id": doc_record.id,
                "file_name": file_name,
                "file_size_bytes": file_size,
                "kriptografi": {
                    "file_hash": new_block.file_hash,
                    "merkle_root": new_block.merkle_root,
                },
                "blockchain": {
                    "block_index": new_block.index,
                    "prev_hash": new_block.prev_hash,
                },
                "penyimpanan": {
                    "ciphertext_path": new_block.ciphertext_path,
                    "status_verifikasi": "VALID"
                }
            }
        })
        
    return JsonResponse({"error": "Harap kirimkan file melalui metode POST dengan key 'document'."}, status=400)