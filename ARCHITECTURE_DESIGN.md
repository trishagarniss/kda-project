### **ARCHITECTURE PAGE**

Design a technical architecture page for a cybersecurity system called CloudGuard EMT (Dynamic AES + Enhanced Merkle Tree + Blockchain Verification).



This page is meant to:

* Educate users about how the system works internally
* Visually explain cryptographic processes
* Present a clear workflow diagram (flowchart) of the entire pipeline



**🎨 VISUAL STYLE**

* Style: Technical diagram + modern SaaS UI
* Feel: Clean, academic, structured, intelligent
* Inspiration:

&#x09;System design diagrams (like AWS architecture)

&#x09;Flowchart UI

&#x09;Developer documentation pages (Stripe / Vercel)



**🎨 COLOR SYSTEM (CONSISTENT)**

Use same palette:

* Background: #0B1120
* Card/Panel: #1E293B
* Border: #334155
* Primary: #10B981 (main flow)
* Secondary: #06B6D4 (data movement)
* Warning: #F59E0B
* Danger: #EF4444
* Text:

&#x09;Heading: #F8FAFC

&#x09;Body: #94A3B8



**✍️ TYPOGRAPHY**

* Headings: Space Grotesk (bold)
* Body: Inter
* Code/Formula:

&#x09;JetBrains Mono



**📐 LAYOUT STRUCTURE**



**🧭 1. PAGE HEADER**

**Content:**

* **Title:**

&#x09;“System Architecture \& Cryptographic Workflow”

* **Subtitle:**

&#x09;Explain:

&#x09;“This section visualizes how CloudGuard EMT processes, encrypts, and verifies data 	integrity using a hybrid cryptographic approach.”



🔁 2. MAIN FLOWCHART (CORE SECTION – MOST IMPORTANT)

**🔥 MUST BE VISUAL**

Design a horizontal or vertical flowchart diagram showing full pipeline:



**FLOW STEPS:**

1. User Upload File (Pengguna memilih file).
2. SHA-256 Hash Generation (Mengekstrak Hash\_File dari dokumen asli).
3. Deduplication Check (PENTING) ➔ Sistem mengecek Hash\_File di Cloud. Jika file sudah ada, cukup update hak milik (STOP). Jika file baru, lanjut ke Step 4.
4. Dynamic Key Generation (XOR) (Peleburan Hash\_File + Prev\_Block\_Hash).
5. AES-256-GCM Encryption (Mengubah file asli + Key + Nonce menjadi Ciphertext).
6. Ciphertext Chunking (Memotong Ciphertext menjadi balok-balok 1KB).
7. Enhanced Merkle Tree Construction (Melakukan hashing dari bawah ke atas pada setiap balok data).
8. Merkle Root Generation (Menghasilkan 1 segel utama sepanjang 64 karakter).
9. Hybrid Storage ➔ Data dipecah dua:
Public Cloud: Menyimpan Ciphertext \& Nonce.
Private Blockchain: Menyimpan Merkle Root, Hash\_File, \& Prev\_Hash.
10. Verification Process (Smart Auditing) (Bukan sekadar Reverse Flow, melainkan: Prediksi Perilaku ➔ Ambil Chunk Acak ➔ Hitung Ulang Root ➔ Cocokkan dengan Blockchain).



**🎨 FLOW DESIGN**

Each step should be:

* Inside rounded card
* Connected with arrows or lines
* Use colors:

| State      | Color   |

| ---------- | ------- |

| Input      | Cyan    |

| Process    | Emerald |

| Critical   | Amber   |

| Error path | Red     |



**💡 VISUAL ENHANCEMENTS**

* Animated arrows (flow direction)
* Glow effect on active nodes
* Use icons:

File 📄

Hash 🔢

Lock 🔐

Tree 🌳

Chain ⛓️



**🔐 3. DYNAMIC AES SECTION (DETAILED BREAKDOWN)**

**Layout:**

Card with formula visualization

**Content:**

Show formula clearly:

AES Key = SHA256(File) ⊕ Previous Block Hash



The formula must be displayed using a monospace font (JetBrains Mono) and visually highlighted inside a dedicated code-style container.



Apply:

\- Slight background contrast (darker panel)

\- Cyan or emerald glow

\- Center alignment



Example visual emphasis:

\[AES Key = SHA256(File) ⊕ Previous Block Hash]



Additionally:

\- Animate the XOR operation (optional)

\- Show two inputs merging into one output



**Add explanation:**

* XOR operation creates unique key per file
* Prevents key reuse attack

**Visual:**

* Two input boxes → XOR → output key



**🌳 4. ENHANCED MERKLE TREE SECTION**

**Layout:**

Split into 2 parts:



**A. Visual Tree Diagram**

* Bottom: Leaf nodes (chunk hashes)
* Middle: parent hashes
* Top: Merkle Root



**B. Explanation:**

* File → split into chunks
* Each chunk hashed
* Combined recursively

**Highlight:**

“Any change in 1 byte will alter the entire Merkle Root”

**Use:**

* Red highlight for “1 byte change”
* Emerald for “secure state”



**⛓️ 5. BLOCKCHAIN INTEGRATION**

**Layout:**

Card showing chain blocks

**Visual:**

\[Block N-1] → \[Block N] → \[Block N+1]



**Each block contains:**

* Previous Hash
* Merkle Root
* Timestamp



**Explanation:**

* Immutable ledger
* Prevents tampering
* Enables verification tracking



**🔍 6. VERIFICATION FLOW (REVERSE PROCESS)**

**Show flow:**

1. Retrieve ciphertext
2. Recalculate hash
3. Rebuild Merkle Tree
4. Compare Merkle Root
5. Decision:

Match → ✅ Allow decryption

Mismatch → ❌ Block access



⚠️ 7. SECURITY INSIGHT PANEL

**Big statement:**

“A single bit modification invalidates the entire integrity chain.”



Style:

* Dark card
* Red highlight on “single bit”
* Glow effect



**🎯 MICRO INTERACTIONS**

* Hover node → show explanation tooltip
* Click node → expand detail
* Flow lines animate
* Tree nodes pulse on recompute



**🚫 AVOID**

* Overly complex diagrams
* Too much text
* Flat boring boxes (must feel alive)



**🧩 FINAL OUTPUT GOAL**

This page should feel like:

A hybrid between technical documentation + interactive system diagram



**User should:**

* Understand system in < 1 minute
* Be impressed visually
* Trust the system security

