# Agent Docs Disclosure Rules

## Public documentation

Tracked project documentation may contain:

- reusable project workflows;
- architecture and ownership boundaries;
- sanitized failure signatures;
- public runtime requirements;
- commands with placeholders;
- schemas and fictional examples.

## Non-public information

Do not place these values in tracked Agent Docs:

- Git names or personal email addresses used as identity;
- absolute user-home paths;
- hostnames, serial numbers, machine IDs, or session IDs;
- tokens, cookies, passwords, private keys, or credential-bearing URLs;
- private repository URLs or internal infrastructure identifiers;
- full command logs that may contain private values;
- unreviewed runtime observations.

Use placeholders such as `$HOME`, `<user>`, `<repository>`, `<host>`, `<token>`, and `<private-url>` when the shape matters.

## Local storage

If the project implements Agent Workspace, keep local observations under its ignored local, raw, or quarantine paths. Otherwise, use an ignored project-local location chosen by the project. Never invent a tracked local-state convention without project approval.

## Promotion workflow

1. Keep raw observations private.
2. Extract the minimum reusable pattern.
3. Remove identity, infrastructure, credential, and machine-specific values.
4. Put the result in the single document that owns it.
5. Run Agent Docs validation and the project's own disclosure checks.
6. Review the staged diff before committing.
