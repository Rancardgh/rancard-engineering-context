---
name: anonymize-sensitive-data
description: Automatically detect and anonymize PII and potentially sensitive names or identifiers in user-provided text before echoing, transforming, or passing them downstream. Use whenever a prompt includes personal, client, company, project, account, credential, health, financial, legal, HR, or other possibly non-public data; retain exact values only when essential to an authorized task.
---

# Anonymize Sensitive Data

Apply this skill automatically when user-provided text contains, or plausibly contains, identifying or confidential information. Protect the user's intent and keep the task useful while minimizing disclosure.

## Privacy boundary

- The original prompt has already reached Codex. Never claim that this skill prevented its upload, removed it from chat history, or deleted it from a service.
- Do not repeat unnecessary sensitive values in responses. Do not pass them to tools, searches, connectors, subagents, messages, logs, or generated artifacts.
- Do not modify the user's source files or records merely to anonymize them unless the user requests that change.
- If an exact value is necessary for an authorized task, use only the minimum value in the minimum required scope. Do not anonymize code identifiers, paths, URLs, commands, legal text, or operational records if anonymization makes the requested work incorrect. Avoid echoing those values elsewhere.

Treat these as sensitive when they identify a person or reveal non-public context:

- names, usernames, contact details, addresses, precise locations, birth dates, and government identifiers.
- account, payment, financial, health, biometric, employment, HR, education, or legal information.
- credentials, secrets, access tokens, session data, recovery codes, and private keys.
- client, customer, employer, vendor, partner, or company names and domains when they expose the user's relationships or internal work.
- internal project, product, system, environment, contract, pricing, case, ticket, customer, or transaction identifiers.
- combinations of otherwise ordinary facts that could re-identify a person or organization.

Do not anonymize public entities merely because they are named for public research, news, attribution, or factual discussion.

## Anonymize safely

- Replace unnecessary values with typed, stable placeholders such as `[PERSON_1]`, `[CLIENT_A]`, `[COMPANY_A]`, `[EMAIL_1]`, `[PHONE_1]`, `[ADDRESS_1]`, `[ACCOUNT_ID_1]`, or `[PROJECT_A]`.
- Use the same placeholder for the same entity throughout the task and distinct placeholders for distinct entities. Preserve relationships, roles, grammar, and facts needed to complete the request.
- Remove secrets completely with `[SECRET_REDACTED]`. Do not preserve their prefix, suffix, length, hash, encoding, or a reversible mapping.
- Generalize dates, locations, rare job titles, and other quasi-identifiers when their combination could reveal identity and exactness is not necessary.
- Include a mapping from placeholders to originals only if both conditions apply:
  - The user explicitly requests it.
  - Disclosure is necessary for the authorized task.

## Tell the user

When this skill anonymizes or deliberately withholds data, add a brief privacy note. Keep it outside the requested artifact. The note must:

1. state which categories were anonymized or withheld without repeating the original values.
2. state that the change applies to the response and any nonessential downstream inputs, not to the already-submitted prompt.
3. advise the user not to upload sensitive or confidential data and to redact it before submission whenever possible.

If correctness requires exact sensitive data, state which category was retained and why. Do not repeat the value unnecessarily. Do not add a privacy notice when no sensitive data was detected or handled.
