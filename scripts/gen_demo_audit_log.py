#!/usr/bin/env python3
"""Generate a canonical OUTPUT_CONTRACT-conformant audit.log for the demo run-dir.

Emits 3 events (convert, records-import, verify) with proper genesis prev_hash
+ chained signatures. Replaces the hand-built audit.log that fails verify_audit_log()
per Bob's code review C1 (agent-collab@<bob-review-commit>).

Run: python3 scripts/gen_demo_audit_log.py > run-dir/audit.log
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

GENESIS_PREV_HASH = "0" * 64


def event_signature(event: dict[str, Any]) -> str:
    """SHA256 of canonical JSON of the event WITHOUT the 'signature' field."""
    body = {k: v for k, v in event.items() if k != "signature"}
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def emit_event(
    subcommand: str,
    inputs: dict[str, Any],
    outputs: dict[str, Any],
    summary: dict[str, Any],
    timestamp: str,
    prev_hash: str,
) -> dict[str, Any]:
    event = {
        "subcommand": subcommand,
        "inputs": inputs,
        "outputs": outputs,
        "summary": summary,
        "timestamp": timestamp,
        "prev_hash": prev_hash,
    }
    event["signature"] = event_signature(event)
    return event


def main() -> None:
    events: list[dict[str, Any]] = []

    e1 = emit_event(
        subcommand="convert",
        inputs={"vault_export_path": "vault-exports/source-tenant.json"},
        outputs={"target_state_path": "target_state.json", "records_count": 3},
        summary={"types_seen": ["login", "databaseCredentials", "sshKeys"], "warnings": 0},
        timestamp="2026-04-30T10:00:00Z",
        prev_hash=GENESIS_PREV_HASH,
    )
    events.append(e1)

    e2 = emit_event(
        subcommand="records-import",
        inputs={"target_state_path": "target_state.json", "tenant": "demo-target"},
        outputs={"records_imported": 3, "records_failed": 0, "manifest_path": "manifest.csv"},
        summary={"created": 3, "skipped": 0, "errored": 0},
        timestamp="2026-04-30T10:05:00Z",
        prev_hash=e1["signature"],
    )
    events.append(e2)

    e3 = emit_event(
        subcommand="verify",
        inputs={"run_dir": "."},
        outputs={"verify_status": "pass", "report_path": "verify-reports/run-2026-04-30.json"},
        summary={"checks_passed": 3, "checks_failed": 0},
        timestamp="2026-04-30T10:10:00Z",
        prev_hash=e2["signature"],
    )
    events.append(e3)

    for event in events:
        print(json.dumps(event, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
