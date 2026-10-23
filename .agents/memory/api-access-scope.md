---
name: Trusted-operator API scope
description: Security boundary chosen when making the imported backend reachable.
---

Treat this setup as a private trusted-operator API, not a public multi-user app.

**Why:** The import has server-key-backed profile reads and writes but no user
identity or ownership model. Starting a reachable workflow would otherwise
expose those operations to unauthenticated callers.

**How to apply:** Keep data operations fail-closed behind operator authentication.
Do not share the operator token with ordinary users or embed it in a frontend.
Before enabling multi-user access, add individual identity and enforce profile
ownership on every read and write. Service health alone does not prove the
profile-to-match flow; approved writes and paid inference are separate checks.
