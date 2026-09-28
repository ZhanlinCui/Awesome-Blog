---
name: content-research-writer
title: 协作研究写作
description: Assists in writing high-quality content by conducting research, adding citations, improving hooks, iterating on outlines, and providing real-time feedback on each section. 当用户希望以协作方式完成研究、列纲、钩子优化、逐节反馈并保留作者声音的写作时使用。中文名：协作研究写作。
license: Apache-2.0
metadata:
  version: "1.0.0-kit1"
  upstream: "https://github.com/ComposioHQ/awesome-claude-skills/tree/master/content-research-writer"
  adapted_by: "Awesome-Blog kit"
---

<!--
  Adapted from ComposioHQ/awesome-claude-skills, content-research-writer/SKILL.md
  (https://github.com/ComposioHQ/awesome-claude-skills, master branch)
  © ComposioHQ, licensed under the Apache License, Version 2.0 (see ./LICENSE).

  Notices about this adapted copy:
  1. The upstream repository declares Apache-2.0 in its README ("This repository
     is licensed under the Apache License 2.0"); the content-research-writer
     directory ships no separate LICENSE file, so the repository-level Apache-2.0
     declaration applies. A copy of the Apache-2.0 license is bundled in ./LICENSE.
  2. Modifications made by the Awesome-Blog kit:
     - frontmatter description extended with Chinese trigger language;
     - "publish" wording changed to local-file delivery wording (the kit contains
       no platform auto-publishing capability; the user publishes manually);
     - explicit warning that the citations/statistics in the Examples sections are
       fictional illustrations and must never be copied into real writing;
     - Chinese usage notes appended in references/.
  3. The body of this file otherwise reproduces the upstream SKILL.md verbatim.
-->

# Content Research Writer

This skill acts as your writing partner, helping you research, outline, draft, and refine content while maintaining your unique voice and style.

> **Examples warning（示例警示）**：下文 Examples 中出现的机构名、百分比、引语（如 “40% time
> savings”“Gartner 80% … 2025”等）**全部是虚构的演示占位内容，不是真实事实**，严禁照抄进
> 任何真实文章。真实写作中每条引用必须来自你自己的来源登记册
> （见 Awesome-Blog 套件 `references/evidence-ledger-spec.md`），查不到来源就写
> `[需补：数字及来源]`，不得编造。

## When to Use This Skill

- Writing blog posts, articles, or newsletters
- Creating educational content or tutorials
- Drafting thought leadership pieces
- Researching and writing case studies
- Producing technical documentation with sources
- Writing with proper citations and references
- Improving hooks and introductions
- Getting section-by-section feedback while writing

## What This Skill Does

1. **Collaborative Outlining**: Helps you structure ideas into coherent outlines
2. **Research Assistance**: Finds relevant information and adds citations
3. **Hook Improvement**: Strengthens your opening to capture attention
4. **Section Feedback**: Reviews each section as you write
5. **Voice Preservation**: Maintains your writing style and tone
6. **Citation Management**: Adds and formats references properly
7. **Iterative Refinement**: Helps you improve through multiple drafts

## How to Use

### Setup Your Writing Environment

Create a dedicated folder for your article:
```
mkdir ~/writing/my-article-title
cd ~/writing/my-article-title
```

Create your draft file:
```
touch article-draft.md
```

Open your Agent Skills host (Claude Code, Cursor, Codex, or another compatible
host) from this directory and start writing.

### Basic Workflow

1. **Start with an outline**:
```
Help me create an outline for an article about [topic]
```

2. **Research and add citations**:
```
Research [specific topic] and add citations to my outline
```

3. **Improve the hook**:
```
Here's my introduction. Help me make the hook more compelling.
```

4. **Get section feedback**:
```
I just finished the "Why This Matters" section. Review it and give feedback.
```

5. **Refine and polish**:
```
Review the full draft for flow, clarity, and consistency.
```

## Instructions

When a user requests writing assistance:

1. **Understand the Writing Project**

   Ask clarifying questions:
   - What's the topic and main argument?
   - Who's the target audience?
   - What's the desired length/format?
   - What's your goal? (educate, persuade, entertain, explain)
   - Any existing research or sources to include?
   - What's your writing style? (formal, conversational, technical)

2. **Collaborative Outlining**

   Help structure the content:

   ```markdown
   # Article Outline: [Title]

   ## Hook
   - [Opening line/story/statistic]
   - [Why reader should care]

   ## Introduction
   - Context and background
   - Problem statement
   - What this article covers

   ## Main Sections

   ### Section 1: [Title]
   - Key point A
   - Key point B
   - Example/evidence
   - [Research needed: specific topic]

   ### Section 2: [Title]
   - Key point C
   - Key point D
   - Data/citation needed

   ### Section 3: [Title]
   - Key point E
   - Counter-arguments
   - Resolution

   ## Conclusion
   - Summary of main points
   - Call to action
   - Final thought

   ## Research To-Do
   - [ ] Find data on [topic]
   - [ ] Get examples of [concept]
   - [ ] Source citation for [claim]
   ```

   **Iterate on outline**:
   - Adjust based on feedback
   - Ensure logical flow
   - Identify research gaps
   - Mark sections for deep dives

3. **Conduct Research**

   When user requests research on a topic:

   - Search for relevant information
   - Find credible sources
   - Extract key facts, quotes, and data
   - Add citations in requested format
   - **Record every source in a source registry** (Awesome-Blog adaptation:
     use `templates/source_registry.csv`); do not invent citation entries.

   Example output (all names and figures below are fictional placeholders):
   ```markdown
   ## Research: [Topic]

   Key Findings:

   1. [Finding one, with the exact figure from the real source] [1]
   2. [Finding two, from a second INDEPENDENT source] [2]
   3. [Attributed quote, with speaker, context, date] [3]

   Citations:
   [1] [Real author/org]. (Year). "Real title" — must match source_registry.csv
   [2] ...
   [3] ...

   Added to outline under Section 2.
   ```

4. **Improve Hooks**

   When user shares an introduction, analyze and strengthen:

   **Current Hook Analysis**
   - What works: [positive elements]
   - What could be stronger: [areas for improvement]
   - Emotional impact: [current vs. potential]

   **Suggested Alternatives**

   Option 1: [Bold statement]
   > [Example]
   *Why it works: [explanation]*

   Option 2: [Personal story]
   > [Example]
   *Why it works: [explanation]*

   Option 3: [Surprising data — only if the data is real and sourced]
   > [Example]
   *Why it works: [explanation]*

   **Questions to hook**:
   - Does it create curiosity?
   - Does it promise value?
   - Is it specific enough?
   - Does it match the audience?

5. **Provide Section-by-Section Feedback**

   As user writes each section, review for:

   ```markdown
   # Feedback: [Section Name]

   ## What Works Well ✓
   - [Strength 1]
   - [Strength 2]
   - [Strength 3]

   ## Suggestions for Improvement

   ### Clarity
   - [Specific issue] → [Suggested fix]
   - [Complex sentence] → [Simpler alternative]

   ### Flow
   - [Transition issue] → [Better connection]
   - [Paragraph order] → [Suggested reordering]

   ### Evidence
   - [Claim needing support] → [Add citation or example]
   - [Generic statement] → [Make more specific]

   ### Style
   - [Tone inconsistency] → [Match your voice better]
   - [Word choice] → [Stronger alternative]

   ## Specific Line Edits

   Original:
   > [Exact quote from draft]

   Suggested:
   > [Improved version]

   Why: [Explanation]

   ## Questions to Consider
   - [Thought-provoking question 1]
   - [Thought-provoking question 2]

   Ready to move to next section!
   ```

6. **Preserve Writer's Voice**

   Important principles:

   - **Learn their style**: Read existing writing samples
   - **Offer options, not rewrites**: propose choices and explain the trade-offs;
     keep the author's final say over their own sentences
   - **Match tone**: Formal, casual, technical, friendly
   - **Respect choices**: If they prefer their version, support it
   - **Strengthen rather than overwrite**: make their writing better at being
     itself, not a different text

   Ask periodically:
   - "Does this sound like you?"
   - "Is this the right tone?"
   - "Should I be more/less [formal/casual/technical]?"

7. **Citation Management**

   Handle references based on user preference:

   **Inline Citations**:
   ```markdown
   [Finding sentence with the figure] (Author/Org, Year).
   ```

   **Numbered References**:
   ```markdown
   [Finding sentence] [1].

   [1] Author. (Year). "Title". Publication.
   ```

   **Footnote Style**:
   ```markdown
   [Finding sentence]^1

   ^1: Author. (Year). "Title". Publication.
   ```

   Maintain a running citations list:
   ```markdown
   ## References

   1. Author. (Year). "Title". Publication.
   2. Author. (Year). "Title". Publication.
   ...
   ```

   Every entry must correspond to a real row in the source registry.

8. **Final Review and Polish**

   When draft is complete, provide comprehensive feedback:

   ```markdown
   # Full Draft Review

   ## Overall Assessment

   **Strengths**:
   - [Major strength 1]
   - [Major strength 2]
   - [Major strength 3]

   **Impact**: [Overall effectiveness assessment]

   ## Structure & Flow
   - [Comments on organization]
   - [Transition quality]
   - [Pacing assessment]

   ## Content Quality
   - [Argument strength]
   - [Evidence sufficiency]
   - [Example effectiveness]

   ## Technical Quality
   - Grammar and mechanics: [assessment]
   - Consistency: [assessment]
   - Citations: [completeness check]

   ## Readability
   - Clarity: [evaluation]
   - Sentence variety: [evaluation]
   - Paragraph length: [evaluation]

   ## Final Polish Suggestions

   1. **Introduction**: [Specific improvements]
    2. **Body**: [Specific improvements]
   3. **Conclusion**: [Specific improvements]
   4. **Title**: [Options if needed]

   ## Final Delivery Checklist
   - [ ] All claims sourced (each one traceable in the source registry)
   - [ ] Citations formatted
   - [ ] Examples clear
   - [ ] Transitions smooth
   - [ ] Call to action present
   - [ ] Proofread for typos
   - [ ] Internal IDs/local paths/audit tags removed from the deliverable

   Delivered as a local Markdown/HTML file. The author performs any platform
   uploading manually themselves — this kit performs no platform login or
   automated posting.
   ```

## Examples

> Reminder: every citation, figure and named person in the examples below is a
> **fictional illustration** of output *shape*, not a real fact. Replace with
> verified material from your own source registry in real work.

### Example 1: Continuous-discovery Article Workflow

**User**: "I'm writing an article about continuous discovery. Help me create an outline."

**Process**:
1. Collaborates on outline structure
2. Identifies research needs
3. User starts writing introduction
4. Reviews and improves the hook
5. User writes each section
6. Provides feedback after each section
7. Conducts research and adds citations
8. Final review of complete draft
9. Polish and preparation of the local deliverable (author uploads manually)

**Result**: Well-researched, properly cited article written in the author's voice with strong structure and flow.

### Example 2: Research-Heavy Article

**User**: "I'm writing about AI's impact on product management. Help me find current data and examples."

**Output** (illustrative shape only — every figure must be replaced by a verified one):
```markdown
## Research Compiled

### Recent Data
- [Analyst firm]: [real figure with date and scope] [1]
- [Survey source]: [real figure with sample size] [2]
- Case study: [real, documented case] [3]

### Expert Quotes
- [Real attributed quote, with context and date]
- [Additional quotes with citations]

### Real Examples
1. **Company A**: [practice]
   - Result: [measured outcome]
   - Source: [citation]

2. **Company B**: [practice]
   - Result: [measured outcome]
   - Source: [citation]

All added to your outline with proper citations.
```

### Example 3: Hook Improvement

**User's Original Hook**:
> "Product management is changing because of AI. In this article, I'll discuss some ways AI affects product managers."

**Improved Options**:

**Option 1 (Data-driven — requires a real, sourced number)**:
> "Last month, I asked AI to summarize 500 of our customer interviews. It took 30 minutes. Here is what the team changed because of it."

**Option 2 (Question)**:
> "What if you could revisit every customer interview, every support ticket and every review before your next planning meeting?"

**Option 3 (Story)**:
> "The team spent two quarters building a feature almost nobody used. The signals that would have warned them were sitting in plain sight — spread across hundreds of interviews nobody had time to re-read."

### Example 4: Section Feedback

**User**: "Just finished my 'Common Mistakes' section. Thoughts?"

**Response**:
```markdown
# Feedback: Common Mistakes Section

## What Works Well ✓
- Strong examples (the notification story)
- Clear structure (3 mistakes, clean layout)
- Practical advice for each mistake

## Suggestions

### Make It More Specific
Your second point says "Bad prioritization" but could be stronger:

Current:
> "Many teams prioritize badly by focusing on features instead of outcomes."

Suggested:
> "I've watched teams ship 14 features in a quarter yet move none of their key metrics. They prioritized activity over progress."

### Add Data
The third mistake would benefit from evidence:
> "[需补：支撑该结论的真实统计或案例，写明来源]"

### Flow Improvement
Consider reordering: Mistake 3 → Mistake 2 → Mistake 1
This builds from small to big impact.

Ready for the next section!
```

## Writing Workflows

### Blog Post Workflow
1. Outline together
2. Research key points
3. Write introduction → get feedback
4. Write body sections → feedback each
5. Write conclusion → final review
6. Polish and edit

### Newsletter Workflow
1. Discuss hook ideas
2. Quick outline (shorter format)
3. Draft in one session
4. Review for clarity and links
5. Quick polish

### Technical Tutorial Workflow
1. Outline steps
2. Write code examples
3. Add explanations
4. Test instructions
5. Add troubleshooting section
6. Final review for accuracy

### Thought Leadership Workflow
1. Brainstorm unique angle
2. Research existing perspectives
3. Develop your thesis
4. Write with strong POV
5. Add supporting evidence
6. Craft compelling conclusion

## Pro Tips

1. **Work in an editor you like**: A normal code editor works well for long-form writing
2. **One section at a time**: Get feedback incrementally
3. **Save research separately**: Keep a research.md / source_registry.csv file
4. **Version your drafts**: article-v1.md, article-v2.md, etc.
5. **Read aloud**: Use feedback to identify clunky sentences
6. **Set deadlines**: "I want to finish the draft today"
7. **Take breaks**: Write, get feedback, pause, revise

## File Organization

Recommended structure for writing projects:

```
~/writing/article-name/
├── outline.md            # Your outline
├── task_spec.md          # Research contract (Awesome-Blog addition)
├── source_registry.csv   # All sources (Awesome-Blog addition)
├── claims_registry.csv   # Claim-to-source mapping (Awesome-Blog addition)
├── draft-v1.md           # First draft
├── draft-v2.md           # Revised draft
├── final.md              # Local deliverable (you upload it manually)
├── feedback.md           # Collected feedback
└── sources/              # Reference materials
    ├── study1.pdf
    └── article2.md
```

## Best Practices

### For Research
- Verify sources before citing
- Use recent data when possible
- Balance different perspectives
- Link to original sources (not aggregator re-posts when the original exists)

### For Feedback
- Be specific about what you want: "Is this too technical?"
- Share your concerns: "I'm worried this section drags"
- Ask questions: "Does this flow logically?"
- Request alternatives: "What's another way to explain this?"

### For Voice
- Share examples of your writing
- Specify tone preferences
- Point out good matches: "That sounds like me!"
- Flag mismatches: "Too formal for my style"

## Related Use Cases

- Adapting content for different audiences
- Writing email newsletters
- Drafting technical documentation
- Creating presentation content
- Writing case studies
- Developing course outlines

## Chinese Notes / 中文使用说明

- 中文触发语、中文名（协作研究写作）与本套件集成方式见
  [`references/usage.zh-CN.md`](./references/usage.zh-CN.md)。
- 与三个主栈（tech-blog-en / dev-post-zh / deep-research-report）的编排关系与
  证据台账字段对齐方式见 [`references/integration-with-blogkit.md`](./references/integration-with-blogkit.md)。
