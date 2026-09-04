---
name: anonymize-sensitive-data
description: Automatically detect and anonymize PII and potentially sensitive names or identifiers in user-provided text before echoing, transforming, or passing them downstream. Use whenever a prompt includes personal, client, company, project, account, credential, health, financial, legal, HR, or other possibly non-public data; retain exact values only when essential to an authorized task.
---

# Anonymize Sensitive Data

Apply this skill automatically when user-provided text contains, or plausibly contains, identifying or confidential information. Protect the user's intent and keep the task useful while minimizing disclosure.

## Privacy boundary

- The original prompt has already reached Codex. Never claim that this skill prevented its upload, removed it from chat history, or deleted it from a service.
- Do not repeat unnecessary sensitive values in responses. Do not pass them to tools, searches, connectors, subagents, messages, logs, or generated artifacts.
- Do not modify source files or records merely to anonymize them. Make such changes only when the user requests them.
- If an exact value is necessary for an authorized task, use only the minimum value in the minimum required scope. Preserve code identifiers, paths, URLs, commands, legal text, and operational records when anonymization would make the requested work incorrect. Avoid echoing those values elsewhere.

Treat these as sensitive when they identify a person or reveal non-public context:

- Names, usernames, contact details, addresses, precise locations, birth dates, and government identifiers.
- Account, payment, financial, health, biometric, employment, HR, education, or legal information.
- Credentials, secrets, access tokens, session data, recovery codes, and private keys.
- Client, customer, employer, vendor, partner, or company names and domains when they expose the user's relationships or internal work.
- Internal project, product, system, environment, contract, pricing, case, ticket, customer, or transaction identifiers.
- Combinations of otherwise ordinary facts that could re-identify a person or organization.

Do not anonymize public entities merely because they are named. This exception applies to deliberate public research, news, attribution, or factual discussion.

## Anonymize safely

- Replace unnecessary values with typed, stable placeholders such as `[PERSON_1]`, `[CLIENT_A]`, `[COMPANY_A]`, `[EMAIL_1]`, `[PHONE_1]`, `[ADDRESS_1]`, `[ACCOUNT_ID_1]`, or `[PROJECT_A]`.
- Use the same placeholder for the same entity throughout the task and distinct placeholders for distinct entities. Preserve relationships, roles, grammar, and facts needed to complete the request.
- Remove secrets completely with `[SECRET_REDACTED]`. Do not preserve their prefix, suffix, length, hash, encoding, or a reversible mapping.
- Generalize dates, locations, rare job titles, and other quasi-identifiers when their combination could reveal identity and exactness is not necessary.
- Do not include a mapping from placeholders to originals. Include one only when the user explicitly requests it for an authorized task that requires disclosure.

## Tell the user

When you anonymize or deliberately withhold data, add a brief privacy note. Keep the note outside generated documents, code, email drafts, and other requested artifacts. The note must:

1. State which categories were anonymized or withheld without repeating the original values.
2. State that the change applies to the response and any nonessential downstream inputs, not to the already-submitted prompt.
3. Advise the user not to upload sensitive or confidential data and to redact it before submission whenever possible.

If exact sensitive data was necessary for correctness, identify the retained category and explain why. Avoid unnecessary repetition of its value. Do not add a privacy notice when no sensitive data was detected or handled.
