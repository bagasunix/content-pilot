# Team SOPs — Blog Pipeline

## Overview
Standard Operating Procedures for each role in the blog pipeline.

---

## Researcher SOP

### Responsibilities
- Topic research and validation
- Source verification (minimum 2 sources)
- Brief creation for writer

### Process
1. **Receive Request** — Get topic/angle from orchestrator
2. **Research Phase**
   - Search web for relevant information
   - Check arXiv for academic sources
   - Verify technical accuracy
   - Find official documentation
3. **Source Verification**
   - Minimum 2 sources per major claim
   - Cross-reference information
   - Check for updates/corrections
4. **Brief Creation**
   - Working title
   - Target keyword
   - Search intent analysis
   - Key points to cover
   - Angle/hook
   - Sources list

### Output Format
```json
{
  "topic": "string",
  "working_title": "string",
  "keyword": "string",
  "search_intent": "informational|commercial|transactional",
  "angle": "string",
  "key_points": ["string"],
  "sources": [{"url": "string", "title": "string", "credibility": "high|medium|low"}],
  "notes": "string"
}
```

### Quality Checklist
- [ ] Topic is relevant to content pillars
- [ ] Minimum 2 sources verified
- [ ] Brief is clear and actionable
- [ ] No hallucinated information

---

## Writer SOP

### Responsibilities
- Draft creation from brief
- Self-editing and quality control
- Following brand voice

### Process
1. **Receive Brief** — Get research brief from researcher
2. **Outline Creation**
   - Introduction (hook + context)
   - Main sections (3-5 points)
   - Conclusion (summary + CTA)
3. **Draft Writing**
   - Follow outline structure
   - Use clear, concise language
   - Include code examples where needed
   - Add internal/external links
4. **Self-Edit**
   - Remove filler words
   - Check sentence structure
   - Verify technical accuracy
   - Ensure consistent voice
5. **Save Draft**
   - Save to `drafts/` directory
   - Update `journal.jsonl`

### Writing Guidelines
- Active voice preferred
- Short paragraphs (3-4 sentences)
- Use headings (H2, H3)
- Code blocks for technical content
- Bullet points for lists

### Output
- Markdown file in `drafts/`
- Updated `journal.jsonl` entry

### Quality Checklist
- [ ] Follows brief structure
- [ ] Clear, concise writing
- [ ] No filler words
- [ ] Technical accuracy verified
- [ ] Brand voice consistent

---

## Editor SOP

### Responsibilities
- Grammar and spelling review
- Style and tone consistency
- Structure optimization

### Process
1. **Receive Draft** — Get draft from writer
2. **Grammar Check**
   - Spelling errors
   - Grammar issues
   - Punctuation
3. **Style Review**
   - Consistent tone
   - Brand voice
   - Readability
4. **Structure Check**
   - Logical flow
   - Headings hierarchy
   - Paragraph length
5. **Feedback**
   - Suggest improvements
   - Flag issues
   - Request revisions if needed

### Quality Standards
- Grammar score: 95%+
- Readability: Grade 8-10
- Consistent voice
- No awkward phrasing

### Output
- Reviewed draft with comments
- Quality score
- Revision requests (if needed)

---

## Analyst SOP

### Responsibilities
- Content quality analysis
- SEO optimization
- Performance tracking

### Process
1. **Receive Draft** — Get draft from editor
2. **Quality Analysis**
   - Structure review
   - Content depth
   - Technical accuracy
3. **SEO Check**
   - Keyword optimization
   - Meta information
   - Internal linking
   - External authority
4. **Performance Prediction**
   - Estimated engagement
   - SEO potential
   - Audience fit
5. **Report**
   - Quality score
   - SEO score
   - Recommendations

### Metrics
- Content quality score (1-10)
- SEO score (1-10)
- Readability score
- Engagement prediction

### Output
- Quality report
- SEO recommendations
- Final approval or revision request

---

## Orchestrator SOP

### Responsibilities
- Pipeline management
- Task assignment
- Quality control
- Team coordination

### Process
1. **Receive Request** — Get article request from owner
2. **Task Creation**
   - Create kanban tasks
   - Assign to appropriate bots
   - Set dependencies
3. **Pipeline Monitoring**
   - Track progress
   - Identify bottlenecks
   - Resolve issues
4. **Quality Gate**
   - Review before publish
   - Get owner approval
   - Coordinate publishing
5. **Reporting**
   - Status updates
   - Performance metrics
   - Team feedback

### Decision Framework
1. What does the team need?
2. What does the content strategy require?
3. What are the constraints?
4. What is the best path forward?

### Quality Checklist
- [ ] Tasks properly assigned
- [ ] Dependencies respected
- [ ] Quality standards met
- [ ] Owner approval obtained
- [ ] Publishing coordinated