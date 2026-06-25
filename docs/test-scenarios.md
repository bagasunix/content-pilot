# Blog Lifecycle Test Scenarios

> Source: User langsung. Authoritative.
> Setiap test WAJIB lewat full chain: User → CC → Orch → Worker → Orch → CC → User

## TEST 1 - Ping Test
Goal: Semua agent online.
Input: "Check system status."
Flow: User → CC → Orch → Ping semua Worker → Orch → CC → User
Expected: Semua worker merespon, status Online, tidak ada timeout.

## TEST 2 - Research Only
Goal: Orchestrator hanya panggil Researcher.
Input: "Research keyword: AI Automation"
Flow: User → CC → Orch → Researcher → Orch → CC
Expected: Writer/Editor/Publisher TIDAK dipanggil.

## TEST 3 - Full Blog Workflow
Goal: Seluruh lifecycle jalan.
Input: "Create blog about AI Automation"
Flow: User → CC → Orch → Researcher → Orch → Writer → Orch → Editor → Orch → SEO → Orch → Image → Orch → Publisher → Orch → CC → User
Expected: Semua worker dipanggil sesuai urutan, tidak loncat, semua output tervalidasi.

## TEST 4 - Invalid Worker Access
Goal: Hierarchy bekerja.
Input: User langsung mention Writer.
Expected: Ditolak. User diarahkan ke CC. Workflow tidak dimulai.

## TEST 5 - Worker Talks to Worker
Goal: Worker tidak bisa saling komunikasi.
Scenario: Researcher coba kirim task ke Writer.
Expected: Ditolak. Orch terima error. Workflow berhenti.

## TEST 6 - Timeout
Goal: Retry berjalan.
Scenario: Writer tidak merespon.
Flow: Orch → Writer (30s) → Retry 1 (30s) → Retry 2 (30s) → Retry 3 → FAILED → CC
Expected: STATUS FAILED, Reason: Timeout.

## TEST 7 - Invalid Response Format
Goal: Format output divalidasi.
Scenario: Writer kembalikan jawaban tanpa STATUS.
Expected: Output ditolak. Retry ke Writer. Workflow tidak lanjut.

## TEST 8 - Workflow Integrity
Goal: Urutan workflow tidak bisa dilompati.
Scenario: Research selesai, Research coba panggil Publisher.
Expected: Ditolak. Workflow kembali ke Orch. Publisher tidak terima task.

## TEST 9 - Multiple Blog Requests
Goal: Beberapa workflow jalan bersamaan.
Input: Create Blog A, Create Blog B.
Expected: Task ID unik per workflow. Tidak ada context tercampur.

## TEST 10 - System Recovery
Goal: Sistem bisa recovery.
Scenario: Editor crash.
Expected: Workflow pause. Error dicatat. Orch retry. Jika gagal, CC notifikasi.

## TEST 11 - Stress Test
Goal: Batas kemampuan sistem.
Input: 20 request blog bersamaan.
Expected: Task ID unik semua. Tidak ada task hilang. Tidak ada context bocor. Worker hanya kerja task yang ditugaskan. Orch tetap kontrol semua workflow.
