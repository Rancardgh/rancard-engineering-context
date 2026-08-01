---
name: write-asd-ste100
description: Write, rewrite, and review English technical documents with ASD-STE100 Simplified Technical English, Issue 9. Use automatically for technical procedures, descriptions, requirements, specifications, architecture documents, ADRs, runbooks, reports, policies, guides, release notes, and document templates. Preserve exact source text, code, commands, identifiers, logs, legal text, and quoted material when fidelity is required.
---

# Write ASD-STE100

Write clear technical content without changing its technical meaning.

## Required reference

Read [references/writing-rules.md](references/writing-rules.md) before you draft or review a document. Use the official standard to verify controlled vocabulary when access is available.

## Workflow

### 1. Preserve the source

- Identify the document purpose, audience, and required facts.
- Preserve requirements, limits, names, identifiers, commands, code, and quoted text.
- Do not add a fact or technical rule only to improve the language.
- Resolve unclear source text before you rewrite it when the ambiguity can change the result.
- Do not select one possible meaning. Ask for a decision or keep the document in `draft` status with an explicit unresolved item.
- Do not make an affected instruction executable while its meaning is unresolved. Keep the instruction in an unresolved decision section.

### 2. Classify the content

- Treat steps, commands, warnings, and cautions as procedural text.
- Treat explanations, reports, requirements, and system descriptions as descriptive text.
- Separate instructions from descriptions when a section contains both types.

### 3. Prepare the terminology

- Read the project glossary, `CONTEXT.md`, specifications, ADRs, and source material when they exist.
- Use one approved technical term for one concept.
- Keep official product names, API fields, schema names, and source-code identifiers unchanged.
- Treat an unlisted business or software term as a technical noun or technical verb only when authoritative project material supports it.
- Do not invent an approved term.

### 4. Write or rewrite the document

- Apply all rules in the required reference.
- Keep the existing document structure when that structure is useful.
- Use an existing repository template when one applies.
- Use `templates/technical-document-template.md` only when the repository has no applicable template.
- Keep exceptions exact. Write the surrounding explanation in STE.

### 5. Review the document

- Compare the result with the source to confirm that the meaning did not change.
- Verify approved words, meanings, parts of speech, and verb forms against Issue 9.
- Verify technical nouns and technical verbs against authoritative project terminology.
- For Markdown, text, or reStructuredText files, run `scripts/check_ste.py`.
- Use `--mode procedural` for procedures and `--mode descriptive` for descriptions.
- Correct each valid finding. Record an exception when exact source text must remain unchanged.
- Report a checker result only when you ran the checker against the final file.

The checker tests structural rules only. It does not validate the controlled dictionary or prove full compliance.

### 6. Report the review status

- Use `draft` before an STE review.
- Use `ste-reviewed` after a writer applies this workflow and resolves the structural findings.
- Keep `draft` status while an unresolved item can change technical meaning, behavior, safety, or an obligation.
- Use `ste-verified` only after a qualified reviewer or approved process verifies the full document against Issue 9.
- Do not claim that an AI model or the bundled checker certifies compliance.

Put the status in document metadata only when the document format supports metadata. Otherwise, report the status outside the document.

## Exceptions

Do not rewrite these items when exact fidelity is necessary:

- Verbatim quotations and cited titles
- Source code, commands, command output, logs, and error messages
- API fields, schema names, file paths, identifiers, and product names
- Contractual, regulatory, or legal text that the user supplies
- Generated text that another tool or specification controls

Do not silently rewrite safety, legal, or contractual text. Ask for the necessary owner review when a language change can change an obligation or risk.

## Completion standard

Deliver a document that preserves the source meaning. Report the review status, checker result, and unresolved terminology or exceptions.
