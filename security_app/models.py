from django.db import models

class SecureDocument(models.Model):
    # Data Asli
    file_name = models.CharField(max_length=255, help_text="Nama file asli yang diupload")
    file_size = models.BigIntegerField(null=True, blank=True, help_text="Ukuran file dalam bytes")
    
    # Data Kriptografi & Blockchain
    file_hash = models.CharField(max_length=64, unique=True, help_text="SHA-256 hash dari file asli")
    merkle_root = models.CharField(max_length=64, help_text="Akar Merkle Tree")
    block_index = models.IntegerField(help_text="Posisi blok di dalam rantai Blockchain")
    prev_hash = models.CharField(max_length=64, help_text="Hash dari blok sebelumnya")
    
    # Audit & Status
    status_verifikasi = models.CharField(
        max_length=20, 
        default="PENDING", 
        choices=[("VALID", "Valid"), ("CORRUPTED", "Corrupted"), ("PENDING", "Pending")]
    )
    
    ciphertext_path = models.CharField(max_length=500, help_text="Lokasi file .bin yang sudah dienkripsi")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Block {self.block_index} | {self.file_name}"