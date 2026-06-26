---
name: parallel-research
description: "Parallel research — riset dari banyak sumber sekaligus menggunakan execute_parallel. Potong waktu research dari sequential ke parallel."
category: content
tags: [research, parallel, multi-source, blog-lifecycle]
---

# Parallel Research

## Kapan Pakai Skill Ini
- Research task membutuhkan data dari 2+ sumber
- Perlu keyword research + competitor analysis + trend analysis
- Blog lifecycle research phase

## Cara Kerja

### Step 1: Definisikan Sumber
Tentukan 3-5 sumber yang mau di-research:
1. Google Search (keyword ideas, search intent)
2. Competitor analysis (top 3 artikel)
3. Forum/Reddit (pain points, pertanyaan umum)
4. YouTube (video populer, angle berbeda)
5. Technical docs (kalau topik teknis)

### Step 2: Parallel Execution
Pakai `execute_parallel` untuk search semua sumber sekaligus:

```python
execute_parallel(tasks=[
    {
        "name": "google_search",
        "command": "web_search 'keyword 1' && web_search 'keyword 2'",
        "timeout": 30
    },
    {
        "name": "competitor_1",
        "command": "web_extract 'https://competitor1.com/artikel'",
        "timeout": 30
    },
    {
        "name": "competitor_2", 
        "command": "web_extract 'https://competitor2.com/artikel'",
        "timeout": 30
    },
    {
        "name": "forum_search",
        "command": "web_search 'site:reddit.com keyword'",
        "timeout": 30
    }
])
```

### Step 3: Rangkum Hasil
Setelah semua parallel task selesai:
1. Kumpulkan semua hasil
2. Identifikasi pattern (apa yang muncul di semua sumber)
3. Extract unique insights dari masing-masing sumber
4. Buat research summary terstruktur

### Step 4: Output Format
Simpan hasil ke workspace/research/<JOB_ID>.md:

```markdown
# Research: <TOPIC>

## Search Intent
- Primary: ...
- Secondary: ...

## Keyword Ideas
1. ... (volume, difficulty)
2. ...
3. ...

## Competitor Analysis
### Artikel 1: <title>
- URL: ...
- Angle: ...
- Strength: ...
- Gap: ...

### Artikel 2: <title>
- ...

## Pain Points (dari forum)
- ...
- ...

## Outline yang Disarankan
1. ...
2. ...
3. ...

## Sources
- [Google Search](...)
- [Competitor 1](...)
- [Reddit](...)
```

## Pitfalls
1. Jangan terlalu banyak parallel task (max 5) — resource intensive
2. Set timeout per task — jangan satu task mati block semua
3. Handle error graceful — kalau 1 sumber gagal, tetap pakai yang lain
4. Jangan langsung copy-paste — rangkum dengan bahasa sendiri
5. Cross-check fakta antar sumber

## Contoh Penggunaan

### Blog Lifecycle Research
```python
# Researcher bot dapat task:
# [JOB:BLG-001][TARGET:researcher][PHASE:research][STATUS:PENDING]
# TOPIC: Tutorial Docker Compose untuk pemula

# Researcher execute parallel:
execute_parallel(tasks=[
    {"name": "keywords", "command": "web_search 'docker compose tutorial pemula'"},
    {"name": "competitor_1", "command": "web_extract 'https://dewaweb.com/blog/docker-compose'"},
    {"name": "competitor_2", "command": "web_extract 'https://niagahoster.co.id/blog/docker-compose'"},
    {"name": "reddit", "command": "web_search 'site:reddit.com docker compose beginner tutorial'"}
])

# Kemudian rangkum semua hasil
```
