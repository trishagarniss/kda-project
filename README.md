# 🛡️ CloudGuard EMT (Enhanced Merkle Tree)

**CloudGuard EMT** adalah purwarupa sistem keamanan data cloud yang mengimplementasikan *Dynamic AES Encryption* untuk kerahasiaan data dan *Enhanced Merkle Tree* (EMT) terintegrasi simulasi *Blockchain* untuk verifikasi integritas data.

Proyek ini dikembangkan sebagai Tugas Akhir/Projek Keamanan Data untuk mendemonstrasikan bagaimana data di lingkungan cloud dapat diamankan dari ancaman modifikasi ilegal dan pencurian kunci enkripsi.

## ✨ Fitur Utama
*   **Dynamic AES-256 Encryption:** Menghasilkan kunci enkripsi dinamis melalui operasi logika XOR antara *hash* file (SHA-256) dengan *hash* dari blok sebelumnya.
*   **Integritas dengan Enhanced Merkle Tree:** Memvalidasi *ciphertext* yang tersimpan di cloud untuk memastikan tidak ada perubahan sekecil 1 bit pun yang dilakukan oleh pihak tidak sah.
*   **Blockchain Metadata Ledger:** Simulasi buku besar (*ledger*) untuk menyimpan *Merkle Root* dan riwayat kunci secara berkesinambungan.
*   **Hacker Terminal View:** Antarmuka simulasi tambahan untuk mendemonstrasikan bagaimana sistem memblokir akses saat *ciphertext* disusupi/dimanipulasi.

## 🗂️ Struktur Direktori
*   `backend/` - Berisi *core engine* kriptografi (AES, SHA-256, Merkle Tree, dan Blockchain Simulator).
*   `frontend/` - Berisi logika *routing* (Flask/FastAPI) dan antarmuka web (HTML/Tailwind).
*   `data/` - Direktori lokal untuk menyimulasikan *cloud storage* (menyimpan *ciphertext* dan file *upload* sementara).
*   `notebooks/` - Jupyter Notebooks untuk pengujian dan purwarupa fungsi kriptografi.

## 🚀 Cara Menjalankan Aplikasi (Local Environment)

Pastikan Python 3.8+ sudah terinstal di sistem Anda (sangat direkomendasikan menggunakan environment Linux/WSL untuk performa optimal).

**1. Clone Repositori & Masuk ke Direktori**
```bash
git clone https://github.com/username/KDA-PROJECT.git
cd KDA-PROJECT
```

**2. Buat Virtual Environment & Aktivasi**

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Instal Dependensi**

```bash
pip install -r requirements.txt
```

**4. Jalankan Server Web**

```bash
python frontend/app.py
```
