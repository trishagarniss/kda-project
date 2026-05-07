import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SecureDocument

# Import mesin kriptografi kalian dari folder core_engine
from .core_engine.crypto_aes import encrypt_file, hash_file, generate_dynamic_key
from .core_engine.blockchain_sim import Blockchain

# Inisialisasi Blockchain CloudGuard
cloudguard_chain = Blockchain()

@csrf_exempt  # Sementara matikan proteksi CSRF agar mudah di-test via API/Postman
def upload_and_secure(request):
    if request.method == 'POST' and request.FILES.get('document'):
        uploaded_file = request.FILES['document']
        file_name = uploaded_file.name
        
        # 1. Simpan file sementara untuk diproses mesin Trisha
        temp_path = f"temp_{file_name}"
        with open(temp_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
                
        # 2. Proses Kriptografi (Domain Trisha)
        file_hash = hash_file(temp_path)
        prev_block = cloudguard_chain.get_last_block()
        prev_hash = prev_block.block_hash
        
        # Generate Kunci AES Dinamis & Lakukan Enkripsi
        key = generate_dynamic_key(file_hash, prev_hash)
        
        # Pastikan folder untuk menyimpan file enkripsi tersedia
        os.makedirs("media/encrypted_vault", exist_ok=True)
        encrypted_path = f"media/encrypted_vault/{file_name}.bin"
        
        encrypt_file(temp_path, key, encrypted_path)
        
        # 3. Catat ke Blockchain (Domain Evan)
        from .core_engine.merkle_tree import build_merkle_tree
        merkle_root = build_merkle_tree(encrypted_path)
        new_block = cloudguard_chain.add_block(file_hash, merkle_root, encrypted_path)
        
        # 4. Simpan Log Permanen ke Supabase (via Django ORM)
        doc_record = SecureDocument.objects.create(
            file_name=file_name,
            file_hash=new_block.file_hash,
            merkle_root=new_block.merkle_root,
            block_index=new_block.index,
            prev_hash=new_block.prev_hash,
            ciphertext_path=new_block.ciphertext_path
        )
        
        # 5. Bersihkan jejak (Hapus file asli yang tidak dienkripsi agar aman)
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return JsonResponse({
            "status": "Sukses",
            "message": "File berhasil diamankan oleh CloudGuard EMT!",
            "data": {
                "file_name": file_name,
                "block_index": new_block.index,
                "merkle_root": new_block.merkle_root,
                "database_id": doc_record.id
            }
        })
        
    return JsonResponse({"error": "Harap kirimkan file melalui metode POST dengan key 'document'."}, status=400)

# buat tombol "audit data" di UI
from .core_engine.merkle_tree import verify_data_integrity
from django.shortcuts import get_object_or_404

@csrf_exempt
def audit_document(request, doc_id):
    if request.method == 'GET':
        doc_record = get_object_or_404(SecureDocument, id=doc_id)

        audit_result = verify_data_integrity(
            ciphertext_path=doc_record.ciphertext_path,
            stored_merkle_root=doc_record.merkle_root
        )

        return JsonResponse({
            "file_name": doc_record.file_name,
            "audit_result": audit_result
        })