# Team Profile Reference

Use this reference before changing developer, machine, session, or Git identity mapping.

## Identity Model

Public files must not contain clear Git names, emails, hostnames, serial numbers, or local IDs.

A local implementation may map the active Git identity to an opaque developer ID through a locally generated salt and fingerprint. The clear Git identity should not be stored if a salted fingerprint is enough.

## Profile Types

- Developer profile: opaque developer ID, actor type, preferences, and linked machine IDs.
- Machine profile: opaque machine ID, linked developer ID, environment facts, and cached capabilities.
- Session profile: opaque session ID linked to one developer and one machine.

Automation identities must remain separate from human developer profiles unless the user explicitly links them through local action.
