# Changelog

All notable changes to `dsk-keepercmd-demo` land here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: this demo repo follows dated, unreleased operational changes.

## [Unreleased]

### Documentation

- README badges now expose Gate 5, nightly rehearsal, and license status.
- Related links now point to DSK's OUTPUT_CONTRACT v1.2 absorption runbook.
- `AGENTS.md` records fixture, Wave 2 gating, and R5.x trailer-policy guidance.

### Tooling

- `.github/stale.yml` adds auto-stale issue/PR review handling with P0/P1/security/blocked exemptions.
- `.github/workflows/no-co-author-trailers.yml` warns on Cursor/Claude `Co-Authored-By` trailers during the R5.x one-week observation window.

### Known gaps

- Real `run-dir-rehearsal16/` fixture is still pending Bob's push; synthetic `run-dir/`
  remains the committed CI fixture.
