#!/usr/bin/env python3
"""Generate a dsk-verifiable audit.log for the demo run-dir.

This mirrors dsk.cli.cmd_import_from_keepercmd._verify_audit_log:

* the genesis ``prev_hash`` is the empty string
* ``signature`` is SHA256(json.dumps(event_without_signature, sort_keys=True))
* the next event's ``prev_hash`` is SHA256 of the full prior JSONL line

There is no production audit emitter in dsk as of this fixture update, so the
generator keeps the verifier's exact hash rules local and explicit.

Run: python3 scripts/gen_demo_audit_log.py > run-dir/audit.log
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from typing import Any

GENESIS_PREV_HASH = ""


def event_signature(event: dict[str, Any]) -> str:
    """Return dsk's signature hash for an event."""
    body = {k: v for k, v in event.items() if k != "signature"}
    canonical = json.dumps(body, sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def event_line(event: dict[str, Any]) -> str:
    """Return the stable JSONL representation used for the chain hash."""
    return json.dumps(event, sort_keys=True, separators=(",", ":"))


def build_event(
    subcommand: str,
    inputs: dict[str, Any],
    outputs: dict[str, Any],
    summary: dict[str, Any],
    timestamp: str,
) -> dict[str, Any]:
    return {
        "subcommand": subcommand,
        "inputs": inputs,
        "outputs": outputs,
        "summary": summary,
        "timestamp": timestamp,
    }


def emit_events(events: Iterable[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    prev_hash = GENESIS_PREV_HASH
    for event in events:
        event["prev_hash"] = prev_hash
        event["signature"] = event_signature(event)
        line = event_line(event)
        lines.append(line)
        prev_hash = hashlib.sha256(line.encode("utf-8")).hexdigest()
    return lines


def main() -> None:
    events = [
        build_event(
            subcommand="convert",
            inputs={"vault_export_path": "vault-exports/source-tenant.json"},
            outputs={"target_state_path": "target_state.json", "records_count": 3},
            summary={"types_seen": ["login", "databaseCredentials", "sshKeys"], "warnings": 0},
            timestamp="2026-04-30T10:00:00Z",
        ),
        build_event(
            subcommand="records-import",
            inputs={"target_state_path": "target_state.json", "tenant": "demo-target"},
            outputs={"records_imported": 3, "records_failed": 0, "manifest_path": "manifest.csv"},
            summary={"created": 3, "skipped": 0, "errored": 0},
            timestamp="2026-04-30T10:05:00Z",
        ),
        build_event(
            subcommand="verify",
            inputs={"run_dir": "."},
            outputs={"verify_status": "pass", "report_path": "verify-reports/run-2026-04-30.json"},
            summary={"checks_passed": 3, "checks_failed": 0},
            timestamp="2026-04-30T10:10:00Z",
        ),
    ]

    for line in emit_events(events):
        print(line)


if __name__ == "__main__":
    main()
