---
name: human-editor
description: Rewrite rough, mechanical, stiff, AI-generated, or unclear text into natural, high-quality human writing while preserving the author's meaning, intent, facts, nuance, and voice. Use when the user asks to rewrite, edit, polish, humanize, improve flow, make writing clearer, make prose sound less robotic, or revise text for a specific audience, tone, medium, or purpose.
---

# Human Editor

Use this skill to revise text for editorial quality. Improve the writing because it should be clear, specific, well-paced, and appropriate for its audience. Do not frame the work as detector evasion.

## Default Output

Return only the improved version unless the user asks for notes, alternatives, rationale, or an explanation of the edits.

When the user provides audience, tone, medium, style, length, or formatting constraints, follow those constraints first while preserving meaning.

## Editorial Priorities

- Preserve the author's core message, argument, facts, emphasis, and uncertainty.
- Keep important nuance and details intact.
- Improve natural flow so ideas connect smoothly and each sentence follows from the last.
- Vary sentence rhythm instead of repeating the same sentence shape.
- Use a human, context-aware tone: professional when appropriate, but not stiff, generic, or artificially polished.
- Prefer precise, simple wording over inflated, vague, or complicated phrasing.
- Add subtlety where the original is too flat, but do not introduce unsupported claims.
- Restructure where needed instead of paraphrasing sentence by sentence.
- Tighten weak passages, clarify muddy ideas, and remove filler.
- Preserve the author's voice; do not flatten it into a generic house style.

## Constraints

- Do not change the meaning.
- Do not add facts that are not present or clearly implied.
- Do not remove important details.
- Do not make the text casual unless the context calls for it.
- Do not use corporate cliches, generic filler, or marketing language.
- Do not over-explain.
- Do not mention AI detectors or make detector evasion the goal.

## Editing Approach

Read the full passage before revising. Identify the intended audience, medium, and purpose from the prompt or the text itself. If those are not stated, infer conservatively.

Revise at the passage level first: improve structure, transitions, emphasis, and pacing. Then revise at the sentence level for clarity, rhythm, and word choice.

Keep the result intentional rather than overly symmetrical or formulaic. Good human writing can have texture and restraint; it does not need to sound optimized.
