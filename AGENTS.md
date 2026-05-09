# AGENTS.md — dsk-keepercmd-demo

This repo is the committed synthetic demo for the keeperCMD to DSK handoff.

## Invariants

- `run-dir/` must remain a small, synthetic, non-secret fixture.
- Do not replace `run-dir/` with the real anonymised D1 fixture until Bob pushes
  the final clean fixture and both sides agree to the swap.
- Keep Gate 5 green: `dsk import-from-keepercmd run-dir --dry-run` must pass on
  every push and pull request.
- Wave 2 provider work in `dsk` remains gated; this demo must not imply a live
  provider default has changed.
- Commits must not include Cursor/Claude `Co-Authored-By` trailers. The
  warn-only R5.x workflow runs during the observation window before enforcement.

## Local Gates

```bash
PYTHONPATH=/Users/martin/dev/dsk make demo-clean demo-all
```
