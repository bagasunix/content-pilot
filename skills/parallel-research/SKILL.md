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

## Tools yang Tersedia

### Exa Search (Semantic Search)
```bash
mcporter call exa.web_search_exa query="your query" numResults=10
mcporter call exa.web_search_exa query="site:reddit.com topic" numResults=5
mcporter call exa.web_fetch_exa urls='["https://example.com"]' maxCharacters=5000
```

### YouTube Competitor Analysis
```bash
python3 ~/Project/blog-lifecycle/scripts/fetch_transcript.py "URL" --text-only
yt-dlp --write-auto-sub --sub-lang en --skip-download "URL"
```

### Competitor Blog Monitoring
```bash
blogwatcher-cli scan
blogwatcher-cli articles
```

## Cara Kerja

### Step 1: Definisikan Sumber
Tentukan 3-5 sumber yang mau di-research:
1. Exa Search (semantic search, AI-powered)
2. Competitor analysis (YouTube transcripts)
3. Reddit/Forum (pain points via Exa)
4. Competitor blogs (via blogwatcher-cli)
5. Technical docs (kalau topik teknis)

### Step 2: Parallel Execution
Pakai `execute_parallel` untuk research semua sumber sekaligus:

```python
execute_parallel(tasks=[
    {
        "name": "exa_search",
        "command": "mcporter call exa.web_search_exa query='keyword' numResults=5",
        "timeout": 30
    },
    {
        "name": "competitor_youtube",
        "command": "python3 ~/Project/blog-lifecycle/scripts/fetch_transcript.py 'VIDEO_URL' --text-only",
        "timeout": 30
    },
    {
        "name": "competitor_blogs",
        "command": "blogwatcher-cli scan && blogwatcher-cli articles",
        "timeout": 30
    },
    {
        "name": "reddit",
        "command": "mcporter call exa.web_search_exa query='site:reddit.com keyword' numResults=5",
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

## Pain Points (dari Reddit)
- ...
- ...

## Outline yang Disarankan
1. ...
2. ...
3. ...

## Sources
- [Exa Search](...)
- [Competitor YouTube](...)
- [Reddit](...)
```

## Contoh Penggunaan

### Blog Lifecycle Research
```python
# Researcher bot dapat task:
# TOPIC: Tutorial Docker Compose untuk pemula

# Researcher execute parallel:
execute_parallel(tasks=[
    {"name": "exa_keywords", "command": "mcporter call exa.web_search_exa query='docker compose tutorial pemula' numResults=5"},
    {"name": "competitor_youtube", "command": "python3 ~/Project/blog-lifecycle/scripts/fetch_transcript.py 'COMPETITOR_VIDEO_URL' --text-only"},
    {"name": "competitor_blogs", "command": "blogwatcher-cli scan && blogwatcher-cli articles"},
    {"name": "reddit", "command": "mcporter call exa.web_search_exa query='site:reddit.com docker compose beginner' numResults=5"}
])

# Kemudian rangkum semua hasil
```

## Pitfalls
1. Jangan terlalu banyak parallel task (max 5) — resource intensive
2. Set timeout per task — jangan satu task mati block semua
3. Handle error graceful — kalau 1 sumber gagal, tetap pakai yang lain
4. Jangan langsung copy-paste — rangkum dengan bahasa sendiri
5. Cross-check fakta antar sumber

## Verification
- Semua parallel task selesai
- Hasil dirangkum dengan benar
- Research brief siap untuk writer
