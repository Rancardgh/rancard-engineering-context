# ASD-STE100 Documentation Policy

## Purpose

Use ASD-STE100 Simplified Technical English to make English technical documents clear, accurate, and consistent.

This policy uses Issue 9, dated January 2025. Issue 9 replaces the prior issues of the standard.

## Scope

Apply this policy when an agent or team member creates, edits, or reviews an English technical document.

The scope includes:

- Procedures and runbooks
- Requirements and specifications
- Architecture documents and Architecture Decision Records (ADRs)
- Technical reports and policies
- API and integration guides
- Release notes and operational guides
- Technical content in document, slide, and PDF files

The policy does not require changes to source code or exact technical values. It also does not require changes to text that another authority controls.

## Required practice

1. Apply `skills/write-asd-ste100/SKILL.md` to all document work in scope.
2. Preserve the technical meaning and all source facts.
3. Use the official Issue 9 writing rules and controlled dictionary.
4. Use project terms from authoritative specifications, glossaries, ADRs, and source material.
5. Use one term for one concept in each domain context.
6. Run the bundled structural checker for supported text files.
7. Complete a manual vocabulary and meaning review before you mark a document as verified.

The official standard is the source of truth. A prompt, language model, or checker does not replace the standard.

## Exceptions

Keep exact text when fidelity is necessary. Common exceptions include:

- Verbatim quotations and cited document titles
- Source code, commands, command output, logs, and error messages
- API fields, schema names, file paths, identifiers, and product names
- Contractual, legal, or regulatory text
- Content that an external specification or generator controls

Apply STE to the text that explains an exception. Record the exception when the document format supports review metadata.

## Review status

Use one of these values when the document format supports review metadata:

- `draft`: The document did not receive a complete STE review.
- `ste-reviewed`: A writer applied the skill and resolved the structural findings.
- `ste-verified`: A qualified reviewer or approved process verified the full document against Issue 9.

Keep `draft` status while an unresolved item can change technical meaning, behavior, safety, or an obligation.

Do not describe a document as certified by the bundled checker or by an AI model.

Safety-critical, contractual, and regulatory documents require review by the responsible human owner.

## Team adoption

Install or copy `skills/write-asd-ste100` into the skill directory of each supported agent.

Add this instruction to each target repository:

```text
Apply the write-asd-ste100 skill automatically when you create, edit, or review an English technical document. Follow the shared ASD-STE100 policy for scope, exceptions, and review status.
```

Keep the policy, skill, checker, and template versions together. Review the setup when ASD publishes a new issue.

## Authoritative sources

- [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf)
- [ASD-STE100 frequently asked questions](https://www.asd-ste100.org/STE_faq.html)
