import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from supabase import create_client, Client
from .models import SecureDocument
from django.shortcuts import render

# Import mesin kriptografi dari folder core_engine
from .core_engine.crypto_aes import encrypt_file, hash_file, generate_dynamic_key, decrypt_file
from .core_engine.blockchain_sim import Blockchain, Block
from .core_engine.merkle_tree import build_merkle_tree, verify_data_integrity

# Inisialisasi Supabase Client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Inisialisasi Blockchain
# cloudguard_chain = Blockchain()

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
        
        if SecureDocument.objects.filter(file_hash=file_hash).exists():
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return JsonResponse({
                "status": "Gagal",
                "message": "File ini sudah pernah diamankan di dalam sistem CloudGuard EMT!"
            }, status=400)
            
        last_doc = SecureDocument.objects.order_by('-block_index').first()

        if last_doc:
            prev_hash = last_doc.file_hash 
            next_index = last_doc.block_index + 1
        else:
            prev_hash = "0" * 64
            next_index = 1
        
        # 3. Proses Kriptografi
        key = generate_dynamic_key(file_hash, prev_hash)
        
        # Simpan file terenkripsi sementara di lokal sblm dilempar ke cloud
        encrypted_temp_path = f"temp_enc_{file_name}.bin"
        encrypt_file(temp_path, key, encrypted_temp_path)
        
        # 4. Hitung Merkle Root
        merkle_root = build_merkle_tree(encrypted_temp_path)
        
        # Catat ke Blockchain
        # new_block = cloudguard_chain.add_block(file_hash, merkle_root, encrypted_path)
        
        # 5. Upload ke Supabase Storage
        file_name_supa = f"{file_name}.bin"
        supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
            path=file_name_supa,
            file=encrypted_temp_path,
            file_options={"content-type": "application/octet-stream"}
        )
        
        # 6. Simpan Metadata ke DB
        doc_record = SecureDocument.objects.create(
            file_name=file_name,
            file_size=file_size,
            file_hash=file_hash,
            merkle_root=merkle_root,
            block_index=next_index,   # Pakai index dari database
            prev_hash=prev_hash,      # Pakai hash dari database
            ciphertext_path=file_name_supa,
            status_verifikasi="VALID" 
        )
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        if os.path.exists(encrypted_temp_path): 
            os.remove(encrypted_temp_path)
            
        return JsonResponse({
            "status": "Sukses",
            "message": "File berhasil diamankan dengan sinkronisasi blockchain permanen!",
            "data": {
                "database_id": doc_record.id,
                "file_name": file_name,
                "file_size_bytes": file_size,
                "kriptografi": {
                    "file_hash": file_hash,
                    "merkle_root": merkle_root,
                },
                "blockchain": {
                    "block_index": next_index,
                    "prev_hash": prev_hash,
                },
                "penyimpanan": {
                    "ciphertext_path": file_name_supa,
                    "status_verifikasi": "VALID"
                }
            }
        })
        
    return JsonResponse({"error": "Harap kirimkan file melalui metode POST dengan key 'document'."}, status=400)

@csrf_exempt
def audit_document(request, doc_id):
    if request.method == 'GET':
        try:
            doc_record = SecureDocument.objects.get(id=doc_id)
            
            # 1. Download file .bin dari Supabase Storage ke temp lokal
            temp_audit_path = f"temp_audit_{doc_record.file_name}.bin"
            try:
                res = supabase.storage.from_(settings.SUPABASE_BUCKET).download(doc_record.ciphertext_path)
                with open(temp_audit_path, 'wb+') as f:
                    f.write(res)
            except Exception:
                return JsonResponse({
                    "status": "Gagal", 
                    "message": "File fisik tidak ditemukan di Cloud Storage."
                }, status=404)
            
            # 2. Jalankan mesin audit Merkle Tree
            audit_result = verify_data_integrity(temp_audit_path, doc_record.merkle_root)
            
            if os.path.exists(temp_audit_path): os.remove(temp_audit_path)
            
            # 3. Update status verifikasi di database
            if audit_result['is_valid']:
                doc_record.status_verifikasi = "VALID"
            else:
                doc_record.status_verifikasi = "CORRUPTED"
            doc_record.save() # Simpan perubahan ke Supabase
            
            # 4. Kirim hasil ke Frontend
            return JsonResponse({
                "status": "Sukses",
                "file_name": doc_record.file_name,
                "audit_detail": audit_result
            })
            
        except SecureDocument.DoesNotExist:
            return JsonResponse({
                "status": "Gagal",
                "message": "Dokumen tidak ditemukan di database."
            }, status=404)
            
@csrf_exempt
def get_all_documents(request):
    if request.method == 'GET':
        documents = SecureDocument.objects.all().order_by('-uploaded_at')
        
        data_list = []
        for doc in documents:
            data_list.append({
                "id": doc.id,
                "file_name": doc.file_name,
                "file_size_bytes": doc.file_size,
                "block_index": doc.block_index,
                "status_verifikasi": doc.status_verifikasi,
                "uploaded_at": doc.uploaded_at.strftime("%Y-%m-%d %H:%M:%S") 
            })
            
        return JsonResponse({
            "status": "Sukses",
            "total_data": len(data_list),
            "data": data_list
        })
        
@csrf_exempt
def audit_network_integrity(request):
    if request.method == 'GET':
        docs = list(SecureDocument.objects.all().order_by('block_index'))
        
        is_safe = True
        
        if len(docs) > 1:
            for i in range(1, len(docs)):
                current_doc = docs[i]
                previous_doc = docs[i-1]
                
                if current_doc.prev_hash != previous_doc.file_hash:
                    is_safe = False
                    break
        
        return JsonResponse({
            "status": "Sukses",
            "network_integrity": "SECURE" if is_safe else "COMPROMISED",
            "message": "Seluruh urutan blok valid dan tidak termanipulasi." if is_safe else "Peringatan! Rantai blok terputus!"
        })
        
@csrf_exempt
def download_decrypted_file(request, doc_id):
    if request.method == 'GET':
        try:
            doc_record = SecureDocument.objects.get(id=doc_id)
            
            temp_cipher_path = f"temp_cipher_{doc_record.file_name}.bin"
            try:
                res = supabase.storage.from_(settings.SUPABASE_BUCKET).download(doc_record.ciphertext_path)
                with open(temp_cipher_path, 'wb+') as f:
                    f.write(res)
            except Exception:
                return JsonResponse({
                    "status": "Gagal", 
                    "message": "File fisik tidak ditemukan di Cloud Storage."
                }, status=404)
            
            key = generate_dynamic_key(doc_record.file_hash, doc_record.prev_hash)
            
            os.makedirs("media/decrypted_vault", exist_ok=True)
            decrypted_path = f"media/decrypted_vault/temp_{doc_record.file_name}"
            
            decrypt_file(temp_cipher_path, key, decrypted_path)
            
            with open(decrypted_path, 'rb') as f:
                file_data = f.read()
                
            if os.path.exists(decrypted_path): 
                os.remove(decrypted_path)
                
            if os.path.exists(temp_cipher_path): 
                os.remove(temp_cipher_path)
                
            response = HttpResponse(file_data, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{doc_record.file_name}"'
            return response
            
        except SecureDocument.DoesNotExist:
            return JsonResponse({
                "status": "Gagal", 
                "message": "Dokumen tidak ditemukan di database."
            }, status=404)
            
        except Exception as e:
            return JsonResponse({
                "status": "Gagal", 
                "message": f"Terjadi kesalahan saat dekripsi: {str(e)}"
            }, status=500)

@csrf_exempt
def tamper_document(request, doc_id):
    if request.method == 'POST':
        try:
            doc = SecureDocument.objects.get(id=doc_id)
            
            # 1. Download ciphertext dari Supabase
            temp_path = f"temp_tamper_{doc.file_name}.bin"
            res = supabase.storage.from_(settings.SUPABASE_BUCKET).download(doc.ciphertext_path)
            with open(temp_path, 'wb') as f:
                f.write(res)
            
            # 2. Flip beberapa byte di tengah file (rusak ciphertext)
            with open(temp_path, 'r+b') as f:
                f.seek(100)  # lewati nonce (12 byte) + sedikit padding
                original = f.read(4)
                f.seek(100)
                f.write(bytes(b ^ 0xFF for b in original))  # XOR flip
            
            # 3. Re-upload file yang sudah dimodifikasi
            supabase.storage.from_(settings.SUPABASE_BUCKET).update(
                path=doc.ciphertext_path,
                file=temp_path,
                file_options={"content-type": "application/octet-stream"}
            )
            
            # 4. Update status di DB
            doc.status_verifikasi = "CORRUPTED"
            doc.save()
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
            return JsonResponse({"status": "Sukses", "message": "File berhasil ditamper."})
            
        except SecureDocument.DoesNotExist:
            return JsonResponse({"status": "Gagal", "message": "Dokumen tidak ditemukan."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "Gagal", "message": str(e)}, status=500)
    
    return JsonResponse({"error": "POST only"}, status=400)

def home_view(request):
    return render(request, 'home.html')

def console_view(request):
    documents = SecureDocument.objects.all().order_by('-uploaded_at')
    
    context = {
        'documents': documents,
        'total_files': documents.count(),
        'corrupted_count': documents.filter(status_verifikasi="CORRUPTED").count(),
    }
    return render(request, 'console.html', context)

def architecture_view(request):
    return render(request, 'architecture.html')

def about_view(request):
    return render(request, 'about.html')