---
name: article-writing-fundamentals
description: Complete article writing skill — structure, hooks, flow, paragraph craft, sentence variety, voice/tone, research workflow, editing/revision, and article type patterns. Foundation for all content creation.
tags: [writing, article, content, editing, copywriting, structure, hooks, revision]
---

# Article Writing Fundamentals

Everything you need to write articles that humans actually want to read.

---

## PART 1: PRINCIPLES (The Non-Negotiables)

### 1.1 The Golden Rules

```
1. CLARITY > CLEVERNESS. If a sentence can be misunderstood, it will be.
2. RESPECT THE READER'S TIME. Every sentence must earn its place.
3. ONE IDEA PER PARAGRAPH. If you need "also" or "additionally" to connect
   two ideas in the same paragraph, split them.
4. SHOW, DON'T TELL. "The server crashed 3 times" > "The server was unreliable."
5. KILL YOUR DARLINGS. That beautiful sentence that doesn't serve the reader? Cut it.
```

### 1.2 The Writing Process (Non-Linear)

```
RESEARCH → DRAFT → DISTANCE → EDIT → POLISH → PUBLISH

- Research:  gather facts, examples, sources (min 30 min for non-trivial topics)
- Draft:     get ideas down, DON'T self-edit yet (that's later)
- Distance:  walk away 15-60 min (or sleep on it)
- Edit:      structural + logic pass (does this make sense?)
- Polish:    sentence-level (rhythm, word choice, grammar)
- Publish:   only after the above
```

---

## PART 2: STRUCTURE

### 2.1 Universal Article Anatomy

```
┌─────────────────────────────────────────────┐
│ HOOK (1-3 sentences)                        │
│ → Grab attention, make a promise, or        │
│   present a problem worth solving           │
├─────────────────────────────────────────────┤
│ CONTEXT / STAKES (2-4 sentences)            │
│ → Why should the reader care? What's the    │
│   cost of NOT reading this?                 │
├─────────────────────────────────────────────┤
│ BODY (main content, 60-80% of article)      │
│ → H2/H3 sections, each with ONE clear idea  │
│ → Evidence, examples, stories per section   │
├─────────────────────────────────────────────┤
│ SYNTHESIS / CLOSE (2-5 sentences)           │
│ → What did we learn? What should the reader │
│   DO next? Memorable closing thought.       │
└─────────────────────────────────────────────┘
```

### 2.2 Structure Patterns

**Pattern A: Inverted Pyramid** (news, updates, announcements)
```
Most important info → supporting details → background
Reader who stops at paragraph 2 still got the value.
```

**Pattern B: Problem → Solution → Proof** (how-to, tutorials)
```
Here's the problem you're facing → Here's how to fix it →
Here's evidence it works (screenshot, data, example)
```

**Pattern C: What → Why → How** (explainers, guides)
```
Define the concept → Explain why it matters → Show how to do it
```

**Pattern D: Narrative / Story Arc** (opinion, case study)
```
Setup (status quo) → Conflict (something broke / changed) →
Resolution (what happened, what we learned) → Takeaway
```

**Pattern E: Listicle with Depth** (top N lists)
```
Each item gets: what it is + WHY this one (not the other 9) +
practical detail that shows you actually used it
Vary depth: spend more words on the best items, less on filler ones.
```

**Pattern F: Comparison** (A vs B)
```
Quick verdict → Deep comparison table → When to choose A vs B →
"Most people should pick X because..."
```

### 2.3 Heading Hierarchy

```
H1: ONE per article. The title. Never another H1 in the body.
H2: Major sections. Each H2 = a complete thought the reader can
    scan and decide "do I need this?"
H3: Sub-sections within an H2. Only when an H2 has multiple
    distinct sub-ideas.

RULE: If you can't write a meaningful H2 for a paragraph,
      it doesn't deserve to be a section — merge it or cut it.
```

---

## PART 3: HOOKS (Opening Lines)

### 3.1 Hook Formulas

**The Cold Open (start mid-action)**
```
"The database was at 98% disk usage. It was 3 AM."
"You've been writing CSS wrong. Here's proof."
```

**The Contrarian**
```
"Most tutorials on X are wrong. Here's why."
"The best way to learn Python isn't tutorials."
```

**The Question (rhetorical or direct)**
```
"What if your deploy pipeline took 2 minutes instead of 20?"
"Why do experienced developers still make this mistake?"
```

**The Stat / Shocking Fact**
```
"73% of production incidents trace back to config changes."
"The average developer spends 42% of their time reading code, not writing it."
```

**The Promise**
```
"In the next 5 minutes, you'll set up a CI/CD pipeline that
 actually works. No Kubernetes required."
```

**The Story / Anecdote**
```
"Last week, I deleted production. Here's what I learned."
"My first code review was so bad my mentor printed it out
 and red-penned every line."
```

### 3.2 Hooks to AVOID

```
❌ "Di era digital yang serba cepat ini..."          (AI tell #1 in Indonesian)
❌ "Sebagai seorang developer..."                    (filler identity claim)
❌ "Pada artikel kali ini, kita akan membahas..."    (announces instead of hooks)
❌ "Halo guys, kali ini..."                          (vlog opening, not article)
❌ "Belakangan ini, banyak orang yang..."            (vague, no specificity)
❌ Starting with a dictionary definition              (nobody cares)
❌ "In today's world..."                             (throat-clearing)
```

### 3.3 The 3-Sentence Rule

```
If your hook hasn't earned the reader's attention in 3 sentences,
you've lost them. Rewrite.

Test: Read ONLY the first 3 sentences aloud. If a stranger
wouldn't keep reading, the hook fails.
```

---

## PART 4: PARAGRAPHS & FLOW

### 4.1 Paragraph Construction

```
TOPIC SENTENCE:   States the paragraph's ONE idea.
SUPPORTING LINES: Evidence, examples, explanation.
LINK TO NEXT:     Subtly sets up what comes next.

Length: 2-5 sentences. If a paragraph exceeds 5 sentences,
break it. If it's 1 sentence, it's either a power move or filler.
```

**Good paragraph (tech article):**
```
"Docker Compose solves the multi-container problem elegantly.
Instead of running 5 separate `docker run` commands with
matching flags, you define everything in one YAML file.
A single `docker compose up` starts your entire stack —
database, API, frontend, cache — in the right order with
the right network. The real win isn't convenience; it's
reproducibility. Your teammate gets the same stack you have."
```

### 4.2 Transitions

**Natural transitions (not mechanical):**
```
❌ "Selanjutnya, kita akan membahas..."     (announcing)
❌ "Poin selanjutnya adalah..."             (listing)
❌ "Moving on to..."                        (dead transition)

✅ Implication: "This works for small projects. At scale, though..."
✅ Question:    "So how do you actually set this up?"
✅ Callback:    "Remember that crashed server? Here's what caused it."
✅ Contrast:    "That's the easy way. The right way is harder."
✅ Continuation: "Once the database is running, the next step is..."
```

### 4.3 Pacing

```
SHORT PARAGRAPHS = fast pace, urgency, punch (good for: hooks, key points)
LONG PARAGRAPHS  = slow pace, depth, explanation (good for: complex topics)

Mix them. A wall of long paragraphs = reader drowns.
A wall of 1-liners = feels shallow.

DIALOGUE / QUOTES = break the rhythm (great for testimonials, expert opinions)
```

---

## PART 5: SENTENCE CRAFT

### 5.1 Sentence Variety

```
SHORT SENTENCE. It punches. Use for emphasis.

Longer sentences that flow and build momentum, carrying the reader
through an idea with enough context to make the next point land.

Then a short one again. Rhythm matters.

COMBINATION RULE: Alternate sentence lengths. Three long sentences
in a row = reader zones out. Ten short ones = feels like a
children's book.
```

### 5.2 Strong vs Weak Writing

```
WEAK:                          STRONG:
"It is important to note       "Note that..."
 that..."

"There are many people who"    "Many people"
 "have..."

"In order to"                  "To"

"Due to the fact that"         "Because"

"at this point in time"        "now" / "currently"

"It should be mentioned"       (delete entirely — just mention it)

"I think that"                 (delete — own your statements)

"Basically" / "Simply"         (if it's simple, the reader knows)

"Very" / "Really"              (cut — use a stronger word instead)
"Weakens everything it touches
```

### 5.3 Active vs Passive

```
PASSIVE: "The config file was edited by the admin."
ACTIVE:  "The admin edited the config file."

PASSIVE USES (intentional):
- When the action matters more than who did it:
  "The server was compromised" (who did it is less important)
- When you don't know who did it:
  "The bug was introduced in commit abc123"
```

### 5.4 Word Economy

```
BEFORE: "It is absolutely essential that developers should always
         make sure to verify their code before pushing."
AFTER:  "Verify code before pushing."

BEFORE: "The reason why this happens is because of the fact that..."
AFTER:  "This happens because..."

RULE: If you can delete a word without changing meaning, delete it.
```

---

## PART 6: VOICE & TONE

### 6.1 Finding Your Voice

```
Voice = WHO you sound like (consistent across articles)
Tone  = HOW you sound (shifts based on topic/context)

Voice examples:
- The Teacher:  patient, explains WHY before HOW, anticipates questions
- The Engineer: precise, shows code, links to docs, no fluff
- The Storyteller: narrative-driven, uses analogies, relatable examples
- The Critic: opinionated, takes stances, backs them up
- The Guide: step-by-step, reassuring, "you got this" energy
```

### 6.2 Tone Spectrum

```
FORMAL ←————————→ CASUAL
   ↑                  ↑
Documentation    Blog posts
Academic         Social content
Legal            Tutorials

MOST BLOG CONTENT: middle-right. Professional but approachable.
"Hey, here's something useful" > "Pursuant to our analysis..."
```

### 6.3 Voice Consistency Check

```
□ Would a reader recognize this as YOUR writing without seeing the byline?
□ Do you have consistent do/don't rules? (e.g., "never use 'utilize'")
□ Does your word choice match your audience? (devs vs marketers vs students)
□ Is your energy level consistent? (don't go casual mid-article then formal)
```

---

## PART 7: RESEARCH & PRE-WRITING

### 7.1 Research Workflow

```
1. UNDERSTAND THE TOPIC (15-30 min)
   - Read 3-5 existing articles on the same topic
   - Note what they cover well AND what they miss
   - Identify YOUR angle (what do you add?)

2. GATHER EVIDENCE (10-20 min)
   - Official docs (primary source)
   - Real-world examples (your experience or documented cases)
   - Data/statistics (with sources)
   - Expert quotes or references

3. BUILD THE BRIEF (5-10 min)
   - Title: what's the promise?
   - Audience: who reads this and what do they already know?
   - Key points: 3-5 things the reader MUST understand
   - Unique angle: why THIS article, not the 100 existing ones?
   - Evidence: what backs up each key point?
```

### 7.2 Brief Template

```markdown
Working Title:    ...
Primary Keyword:  ...
Search Intent:    informational | howto | comparison | opinion
Audience:         who + what they already know
Promise:          what can they DO after reading?
Angle:            what does THIS article say that top 5 SERP results don't?
Key Points:
  1. ...
  2. ...
  3. ...
Evidence:
  - Source 1: ...
  - Source 2: ...
  - Personal experience: ...
Target Length:    ... words
Internal Links:   2-4 related posts
```

### 7.3 What NOT to Do in Research

```
❌ Copy-paste structure from top-ranking article (you become a clone)
❌ Use only one source (bias + shallow)
❌ Skip research because "I already know this" (you'll miss the angle)
❌ Start writing before you know your angle (guaranteed meh article)
```

---

## PART 8: EDITING & REVISION

### 8.1 The 3-Pass Edit

**Pass 1: STRUCTURAL (the macro edit)**
```
Read the whole article. Ask:
□ Does the hook earn attention in 3 sentences?
□ Can I summarize each H2 section in one sentence? (if not, it's unfocused)
□ Is there a logical flow from section to section?
□ Are there sections that don't serve the reader? (CUT THEM)
□ Does the ending deliver on the hook's promise?
□ Right length? (not padding, not rushed)
```

**Pass 2: LINE-LEVEL (the micro edit)**
```
Read paragraph by paragraph. Ask:
□ Does the first sentence of each paragraph state the idea?
□ Are there filler phrases? (see 5.2 weak vs strong)
□ Varied sentence lengths? (rhythm check)
□ Transitions between paragraphs natural?
□ Every claim backed by evidence, example, or clearly marked as opinion?
□ No jargon the audience won't know? (or explained if used)
```

**Pass 3: POLISH (the surface edit)**
```
Read aloud (or use text-to-speech). Ask:
□ Does it sound natural when spoken?
□ Any awkward phrasing? (rewrite those sentences)
□ Consistent style? (Oxford comma, capitalization, terminology)
□ Grammar clean? (subject-verb agreement, dangling modifiers)
□ No repetition? (same idea in different words = cut one)
```

### 8.2 Self-Edit Checklist

```
PRE-DRAFT:
□ Brief written (even a rough one)
□ Angle identified
□ Target audience clear

POST-DRAFT:
□ Hook tested (read first 3 sentences to a stranger — would they continue?)
□ Every H2 is a complete, scannable idea
□ No section longer than 300 words without a sub-break
□ Examples/data in at least 50% of sections
□ Opening doesn't start with "Di era digital..." or similar AI tell
□ Closing delivers value (not just "demikian artikel ini")
□ Word count appropriate for topic depth
□ Filler words removed (very, really, basically, simply, actually)
□ Passive voice minimized
□ No invented facts or unverified claims
```

### 8.3 Common Article Mistakes

```
1. THE THROAT-CLEARER
   Starting with context instead of the hook.
   "Dalam dunia programming, ada banyak bahasa..." → just start.

2. THE MIDDLE DIP
   Strong opening, strong ending, boring middle.
   Fix: add examples, stories, or a concrete demo in the middle.

3. THE LAZY LISTICLE
   "10 Tips for X" where every tip gets exactly 2 paragraphs.
   Fix: spend more words on the best tips, less on filler.

4. THE FACTLESS OPINION
   "I think X is better than Y" without evidence.
   Fix: show benchmarks, code, screenshots, or link to data.

5. THE NEVER-ENDING ARTICLE
   3000 words for a topic that deserves 800.
   Fix: ask "would a reader share this?" — if not, tighten.

6. THE COPY-PASTE STRUCTURE
   Article reads exactly like the top 3 Google results.
   Fix: find YOUR angle before writing.

7. THE HOLLOW CLOSE
   "Semoga artikel ini bermanfaat." → delete immediately.
   Fix: end with a specific action, memorable line, or question.
```

---

## PART 9: ARTICLE TYPE PATTERNS

### 9.1 How-To / Tutorial

```
Structure:
 1. What you'll build/achieve (the promise)
 2. Prerequisites (what they need before starting)
 3. Step-by-step instructions (numbered, imperative)
 4. Expected output at each step (screenshot or code block)
 5. Common errors & troubleshooting
 6. What's next / next steps

KEY RULES:
- Every step must be VERIFIABLE (reader can check it worked)
- Show actual output, not just "it should look like this"
- If a step can fail, explain the error and fix
- Number steps — readers need to track progress
```

### 9.2 Listicle

```
Structure:
 1. Quick intro (what this list covers + why these items)
 2. Items (varied depth — best items get more words)
 3. Quick conclusion (synthesize, don't just recap)

KEY RULES:
- Each item = what it is + WHY it's on this list + practical detail
- Vary depth: top 3 items deserve 3x the words of #8
- Add a verdict/recommendation at the end
- Don't pad with filler items to hit a round number
```

### 9.3 Review / Comparison

```
Structure:
 1. Quick verdict (who should pick what — TL;DR)
 2. Context (what are these things, who are they for?)
 3. Head-to-head comparison (features, price, performance)
 4. Deep dive on key differences
 5. Final recommendation (with reasoning)

KEY RULES:
- Lead with the verdict (readers often just want the answer)
- Be fair: mention strengths AND weaknesses of both
- Use a comparison table for specs/features
- Back opinions with evidence
```

### 9.4 Opinion / Analysis

```
Structure:
 1. The claim (bold, clear, debatable)
 2. Why this matters (stakes)
 3. Evidence (3-5 points supporting your claim)
 4. Counter-arguments (address them honestly)
 5. Synthesis (where you land and why)

KEY RULES:
- State your position clearly (no wishy-washy "maybe")
- Steelman the opposing view before refuting it
- Evidence > opinion (data, examples, expert quotes)
- Acknowledge uncertainty where it exists
```

### 9.5 News / Announcement

```
Structure:
 1. The news (inverted pyramid — most important first)
 2. Details (what changed, why it matters)
 3. Impact (how this affects the reader)
 4. What's next

KEY RULES:
- Lead with the headline fact
- No fluff, no throat-clearing
- Link to primary sources
- Keep it tight (< 800 words usually)
```

---

## PART 10: ADVANCED TECHNIQUES

### 10.1 The "So What?" Test

```
After every paragraph, ask: "So what? Why should the reader care?"
If you can't answer, the paragraph doesn't serve the reader.
Either rewrite it to make the relevance clear, or cut it.
```

### 10.2 Specificity

```
WEAK:   "This tool is very fast."
STRONG: "This tool processes 10K records in 2.3 seconds on a M1 MacBook."

WEAK:   "Many developers struggle with this."
STRONG: "In a 2024 Stack Overflow survey, 47% of developers listed
         debugging as their biggest time sink."

RULE: Replace every vague claim with a specific one.
If you don't have data, use a concrete example instead.
```

### 10.3 Analogies & Metaphors

```
Use when: explaining abstract concepts to a broad audience.

GOOD: "A Docker container is like a shipping container for code —
       it packages your app with everything it needs to run,
       so it works the same anywhere."

BAD:  Overextended metaphors that break down halfway through.

RULE: One clear analogy per concept. Don't mix metaphors.
```

### 10.4 The Curiosity Gap

```
Open a loop early that you close later:

"Three months later, the database crashed. Here's the config
 change that caused it." (reader wants to know WHICH change)

"Don't make the same mistake I did with this Docker setup."
(reader wants to know what the mistake was)

Close every loop you open. Unresolved curiosity = frustrated readers.
```

### 10.5 Scannability (for web articles)

```
- H2s that describe the section (reader decides if they need it)
- Bold key phrases (scanning readers hit bold text first)
- Short paragraphs (2-5 sentences max)
- Lists for 3+ items (not paragraphs)
- Code blocks for code (never inline unless very short)
- Images/screenshots for visual learners
- TL;DR or summary for impatient readers

80% of web readers SCAN before they READ.
Design for the scanner first, the reader second.
```

---

## PART 11: WRITING PROMPTS (Quick Reference)

```
Before writing, answer these:

1. WHO is this for? (specific person, not "everyone")
2. What do they ALREADY know? (don't over-explain basics)
3. What will they DO after reading? (action > information)
4. What's MY unique angle? (not a copy of existing content)
5. What's the ONE sentence takeaway? (if unclear, rewrite the brief)

During writing, ask yourself:

6. Does this sentence earn its place? (cut if not)
7. Would I read this if someone else wrote it? (honesty check)
8. Am I showing or just telling? (evidence > claims)
9. Is the flow natural? (read transitions aloud)
10. Does each section have a clear purpose? (merge unfocused ones)

Before publishing, verify:

11. Hook tested with a real person? (or at least read aloud)
12. Every factual claim sourced or experienced?
13. No AI tell phrases? (see Hook section)
14. Word count appropriate? (not padding, not rushed)
15. CTA or next step clear? (reader knows what to do next)
```
