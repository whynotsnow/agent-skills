# Disclosure Boundaries

## Public Sidecar Content

Tracked sidecar files may contain:

- task titles and sanitized scope;
- reusable decisions;
- plans that do not expose secrets or private runtime details;
- summarized validation outcomes;
- changed relative paths;
- public issue IDs or internal item IDs;
- source commit SHAs when they are safe to reference in the project context.

## Keep Out Of Tracked Sidecar Files

Never persist:

- tokens, passwords, private keys, cookies, session IDs, Access JWTs, or API keys;
- raw command logs that may contain credentials, private paths, private URLs, IPs, or hostnames;
- local Git identities, personal names, emails, machine IDs, profile IDs, or user-home absolute paths;
- unreviewed screenshots or copied page content from private systems;
- production resource IDs when the project policy says they are private;
- private customer, user, or maintainer data not needed for reusable planning.

## Sanitization

Use placeholders when shape matters:

- `$HOME`
- `<user>`
- `<repository>`
- `<host>`
- `<resource-id>`
- `<token>`

Reduce raw output to the smallest stable signal:

- command name;
- pass/fail result;
- short error signature;
- relative file path;
- validation gap or next action.

## Local And Raw Material

If raw observations must be kept temporarily, place them in ignored local/raw/quarantine storage declared by the main project. Do not invent a tracked location for raw diagnostics.

Before promoting any observation into a tracked sidecar file, check that it is reusable, necessary, sanitized, and owned by the sidecar rather than by main project documentation.
