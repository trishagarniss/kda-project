# 🛡️ CloudGuard EMT (Zero-Trust Document Vault)

**CloudGuard EMT** adalah purwarupa sistem keamanan penyimpanan *cloud* berarsitektur *Zero-Trust* yang mengimplementasikan *Dynamic AES Encryption* untuk kerahasiaan data dan *Enhanced Merkle Tree* (EMT) untuk verifikasi integritas (*tamper-proof*). 

Proyek ini dikembangkan sebagai Tugas Akhir mata kuliah **Keamanan Data dan Aplikasinya (KDA)** untuk mendemonstrasikan bagaimana dokumen di lingkungan *cloud* dapat diamankan dari ancaman orang dalam (*insider threat*), modifikasi data senyap (*silent tampering*), dan kebocoran massal (*single point of failure*).

## ✨ Fitur Utama
* **End-to-End Dynamic AES-256-GCM:** Menghasilkan kunci enkripsi unik per dokumen secara dinamis melalui operasi logika XOR antara nilai *hash* SHA-256 dari dokumen saat ini dengan *hash* dokumen sebelumnya (*Forward Secrecy*).
* **Tamper-Proof Integrity (Merkle Tree):** Memecah *ciphertext* menjadi *chunks* dan membangun *Merkle Tree*. Sistem akan langsung memblokir akses dan membunyikan peringatan jika 1 *bit* data di *cloud* terdeteksi diubah oleh pihak luar.
* **Hybrid Storage Architecture:**
* * **Ledger Database:** Metadata, *hash chain*, dan *Merkle Root* disimpan dengan aman di **PostgreSQL (Supabase Database)**.
  * **Vault Storage:** *Ciphertext* berwujud biner (`.bin`) disimpan terpisah di **Supabase Storage**.
* **Interactive Security Console:** Antarmuka bergaya *cyber-terminal* untuk mendemonstrasikan jalur eksekusi kriptografi (Upload ➔ Hash ➔ Dynamic Key ➔ Merkle ➔ Store) secara visual dan interaktif.

## 🛠️ Tech Stack
* **Backend Framework:** Django (Python)
* **Database & Storage:** Supabase (PostgreSQL & Object Storage)
* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
* **Cryptography:** `hashlib`, `cryptography.hazmat.primitives.ciphers` (AES-GCM)

## 🗂️ Struktur Direktori Utama
```text
kda-project/
├── cloudguard_prj/        # Pengaturan utama (settings) konfigurasi Django
├── security_app/          # Aplikasi utama sistem keamanan
│   ├── core_engine/       # Modul inti kriptografi 
│   │   ├── crypto_aes.py  # Logika Hashing, XOR, dan Enkripsi AES-256-GCM
│   │   └── merkle_tree.py # Logika pemotongan file (Chunking) & pembuatan Root
│   ├── models.py          # Skema database untuk Ledger
│   └── views.py           # Endpoint API dan Controller UI
├── templates/             # Antarmuka web (Base, Console, Dashboard, dll)
├── static/                # Aset statis (Gambar, Logo, CSS Tambahan)
└── manage.py              # CLI eksekutor Django
