### **CONSOLE PAGE**

Design a highly interactive cybersecurity control panel (console/workspace) for a system called CloudGuard EMT (Dynamic AES + Enhanced Merkle Tree Blockchain Integrity System).



This page is the core operational dashboard where users upload files, view encryption pipeline execution, and verify integrity.



**🎨 VISUAL STYLE**

* Style: Cybersecurity terminal + modern SaaS dashboard hybrid
* Feel: Hacker console, but clean and enterprise-grade
* Layout inspiration:

&#x09;GitHub Actions UI (pipeline feel)

&#x09;Vercel dashboard

&#x09;Blockchain explorer UI

&#x09;Cyberpunk terminal (subtle, not noisy)





**🎨 COLOR SYSTEM (STRICT)**

Use same palette:

**Background**

* Main: #0B1120

**Panels**

* Cards: #1E293B
* Borders: #334155

**Accents**

* Primary success / encryption OK: #10B981 (emerald)
* Secondary / process flow: #06B6D4 (cyan)
* Warning (integrity issue): #F59E0B
* Danger (hack / tamper): #EF4444

**Text**

* Title: #F8FAFC
* Body: #94A3B8



**✍️ TYPOGRAPHY SYSTEM**

* Headings: Space Grotesk (bold, futuristic)
* Body: Inter (clean UI text)
* Code / cryptographic output:
* JetBrains Mono (VERY IMPORTANT for hashes, keys, nonce, root)





📐 LAYOUT STRUCTURE (CORE DASHBOARD)

Split layout into 3 main zones:

**🧭 1. TOP STATUS BAR (SYSTEM OVERVIEW)**

**Layout:**

Horizontal full-width bar

**Content:**

* System Status:

&#x09;“CloudGuard EMT: ACTIVE” (green indicator dot)

* Blockchain Sync Status
* Last Operation Timestamp
* Integrity Status:

&#x09;OK / Warning / Compromised

* UI Behavior:

&#x09;Green pulse if secure

&#x09;Red glow if tampered detected



**📦 2. MAIN WORKSPACE (CENTER AREA)**

Split into 2 columns:

**🟩 LEFT PANEL: FILE UPLOAD + INPUT**

**A. Upload Box (Drag \& Drop Zone)**

* Large dashed border box
* Text:

&#x09;“Drop file or click to upload”

* Background slightly lighter than main bg

**Interaction:**

* On hover: border turns emerald glow
* On file drop: animation “processing starts”



**B. File Metadata Preview**

After upload show:

* File name
* File size
* File type
* SHA-256 hash (mono font)



**C. Action Button**

* “Process Encryption”
* Style:

&#x09;Emerald background

&#x09;Glow effect on hover

* Disabled state until file uploaded



**🟦 RIGHT PANEL: LIVE OUTPUT DASHBOAR**D

This is the MOST IMPORTANT SECTION visually



**🔐 1. CRYPTO OUTPUT CARDS**

Grid of cards:

**Card 1: SHA-256 Hash**

* Mono font
* Emerald highlight label

**Card 2: Dynamic AES Key**

* Very long string (truncate with expand button)
* Cyan highlight

**Card 3: Nonce**

* Smaller but mono styled



**⚙️ 2. PROCESS PIPELINE VISUALIZER**

Horizontal step tracker:

Upload → SHA-256 → XOR Key Gen → AES Encrypt → Chunking → Merkle Tree → Blockchain Store

**UI Behavior:**

* Each step becomes:

&#x09;Gray = not started

&#x09;Cyan = processing

&#x09;Green = completed

&#x09;Red = failed

* Animated progress line flows left to right



**🌳 3. MERKLE TREE VISUAL SECTION**

* Show simplified tree visualization
* Leaf nodes = ciphertext chunks
* Root node = Merkle Root

**Behavior:**

* If file unchanged → root green
* If tampered → root turns red + shakes animation



**⛓️ 4. BLOCKCHAIN LOG SIMULATION**

* Scrollable log panel
* Each block:

Block #1024

Hash: 9f8a...

PrevHash: 3ab2...

MerkleRoot: a91c...

Status: VERIFIED

**UI Style:**

* Terminal-like
* Alternating dark rows
* Verified = green
* Tampered = red



**⚠️ 3. SECURITY ACTION PANEL (BOTTOM SECTION)**

**🔍 VERIFY BUTTON**

* “Verify Integrity”
* Runs recomputation of hash + Merkle root



**💀 HACK SIMULATION BUTTON (VERY IMPORTANT DEMO FEATURE)**

* Label: “Simulate Data Tampering”
* Effect:

&#x09;Random bit change in ciphertext

&#x09;Merkle root mismatch

&#x09;Entire system turns red warning state



* Before triggering the Merkle Root mismatch, display a short terminal-like animation:



"Injecting bad payload to Supabase Storage..."



* The text should appear with a typing effect, simulating a real system-level attack on external cloud storage.



* After the animation completes:

\- Merkle Root turns red

\- Integrity status changes to "COMPROMISED"

\- Blockchain log updates with a tampered entry





**🧠 OUTPUT ALERT BOX**

Dynamic alert box:

**Success:**

“Integrity Verified. Data is secure.”

**Failure:**

“WARNING: Data tampering detected. Merkle Root mismatch!”



**Style:**

* Success = emerald glow
* Error = red pulse animation



**🎯 MICRO INTERACTIONS (IMPORTANT FOR WOW FACTOR)**

* Buttons glow on hover
* Pipeline animates like loading CI/CD system
* Hash values appear “typing effect”
* Merkle tree nodes animate on recomputation
* Blockchain logs scroll like terminal feed



**🚫 AVOID**

* Too playful UI
* Over-colorful design
* Cartoon icons
* Overloaded animations



**🧩 FINAL OUTPUT GOAL**

This page should feel like:



“A real-world cryptographic security operations dashboard used by a cloud security engineer.”



Not a demo. Not a school project UI.

But a security system control panel.

