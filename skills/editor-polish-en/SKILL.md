---
name: editor-polish-en
title: 英文编辑润色
description: "English-language editing and de-AI-tone pass: diagnose generic AI prose, filler, hype adjectives, rhythm and flow, terminology consistency; propose options without overwriting the author's voice. Use when polishing an English draft or removing generic LLM writing patterns. 中文名：英文编辑润色。"
license: MIT
metadata:
  version: "1.0.0"
  language: en
  kit: awesome-blog
---

# 英文编辑润色（editor-polish-en）

## Operating mode
Diagnose first, prescribe second: name the issue and location → offer ≥2 rewrite
options with trade-offs → author decides. Never overwrite silently. Protected
text (code, commands, identifiers, version numbers, figures) is never altered.

## Generic-AI-prose checklist (scan every paragraph)
1. Filler openings and wind-up: "In today's fast-paced world", "It is worth noting" — cut.
2. Hype adjectives without evidence: revolutionary, seamless, powerful, cutting-edge — replace with the concrete fact or delete.
3. Mechanical triples ("efficient, scalable, and reliable") and forced em-dash asides.
4. Vague attribution ("experts say", "many believe") — source it or remove.
5. Zombie nouns and nominalization ("performs the implementation of" → "implements").
6. Uniform sentence length and rhythm; every sentence starting the same way.
7. Over-hedging chains ("it seems that it might potentially perhaps...") — calibrate to evidence strength.
8. Empty transition soup ("Furthermore/Moreover/Additionally" stacked) vs. missing transitions.
9. Conclusion that merely repeats or ends on a generic CTA — tie back to the hook, state honest limitations and a concrete next step.
10. Density check: claims without numbers/examples go back to research, not to decoration.

## Accuracy safeguards
- Editing must never change the factual meaning; flagged uncertainty goes back to fact-checker.
- Keep non-native authors' genuine voice; the goal is clarity in *their* register, not homogenization.
- Terminology/naming consistency across the whole draft.

## Quality gate
- A polish pass that alters technical claims, touches protected text, or erases the
  author's voice is rejected and redone.

## Not in scope
- No synonym-spinning to evade detectors (do not inject errors); no newly invented facts;
  no publishing actions of any kind — output is a local draft.
