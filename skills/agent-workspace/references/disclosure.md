# Disclosure Reference

Use this reference before promoting runtime observations, preparing a workspace for open source, or changing public/private storage boundaries.

## Public

Public files may be tracked and opened:

- `AGENTS.md` or equivalent public instruction entry.
- Public agent docs.
- Specs, schemas, and sanitized examples.
- Sanitized memory and failure patterns.

## Local

Ignored local files may be read and analyzed when their developer, machine, session, or diagnostic context is relevant to the current task:

- `.agent-workspace/local/`
- `.agent-workspace/raw/`
- `.agent-workspace/quarantine/`

Privacy is an output and persistence boundary, not an access prohibition. Do not inspect local files without a task-relevant reason, and do not reproduce, enumerate, quote, or copy their private values into tracked files or handoffs.

Local state may influence execution and reporting. A handoff may include only the minimum task-relevant, sanitized conclusion, such as capability availability or the class of a runtime limitation. It must not expose identities, paths, hostnames, opaque profile IDs, private URLs, credentials, or raw observations.

## Promotion Rule

Raw observations must be reviewed before becoming public knowledge. Recurrence proves usefulness, not disclosure safety.

Replace private values with placeholders such as `$HOME`, `<user>`, `<repository>`, `<host>`, `<token>`, or `<private-url>`.

Never publish:

- Git names or emails.
- Absolute user-home paths.
- Hostnames, serial numbers, or machine IDs.
- Tokens, cookies, private keys, credentials, or credential-bearing URLs.
- Full logs that may include private paths or infrastructure details.
