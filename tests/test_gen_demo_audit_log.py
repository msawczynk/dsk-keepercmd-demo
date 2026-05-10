"""Regression tests for the synthetic demo audit-log generator."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from typing import Any

import pytest

from dsk.cli.audit_chain import AuditChainCorrupt, verify_audit_log

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "gen_demo_audit_log.py"


def _load_generator() -> Any:
    spec = importlib.util.spec_from_file_location("gen_demo_audit_log", GENERATOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sample_events() -> list[dict[str, Any]]:
    gen = _load_generator()
    return [
        gen.build_event(
            subcommand="convert",
            inputs={"vault_export_path": "vault-exports/source-tenant.json"},
            outputs={"target_state_path": "target_state.json", "records_count": 3},
            summary={"types_seen": ["login", "databaseCredentials"], "warnings": 0},
            timestamp="2026-04-30T10:00:00Z",
        ),
        gen.build_event(
            subcommand="records-import",
            inputs={"target_state_path": "target_state.json", "tenant": "demo-target"},
            outputs={"records_imported": 3, "records_failed": 0, "manifest_path": "manifest.csv"},
            summary={"created": 3, "skipped": 0, "errored": 0},
            timestamp="2026-04-30T10:05:00Z",
        ),
    ]


def _write_audit_log(tmp_path: Path, lines: list[str]) -> Path:
    audit_log = tmp_path / "audit.log"
    audit_log.write_text("\n".join(lines), encoding="utf-8")
    return audit_log


def test_emit_events_generates_dsk_verifiable_audit_log(tmp_path: Path) -> None:
    gen = _load_generator()
    audit_log = _write_audit_log(tmp_path, gen.emit_events(_sample_events()))

    verify_audit_log(audit_log)


def test_emit_events_handles_empty_input(tmp_path: Path) -> None:
    gen = _load_generator()
    lines = gen.emit_events([])

    assert lines == []
    with pytest.raises(AuditChainCorrupt, match="no verifiable entries"):
        verify_audit_log(_write_audit_log(tmp_path, lines))


def test_emit_events_handles_large_input(tmp_path: Path) -> None:
    gen = _load_generator()
    events = [
        gen.build_event(
            subcommand="records-import",
            inputs={"target_state_path": "target_state.json", "tenant": "demo-target"},
            outputs={"records_imported": index, "records_failed": 0, "manifest_path": "manifest.csv"},
            summary={"created": index, "skipped": 0, "errored": 0},
            timestamp=f"2026-04-30T10:{index % 60:02d}:00Z",
        )
        for index in range(250)
    ]
    audit_log = _write_audit_log(tmp_path, gen.emit_events(events))

    verify_audit_log(audit_log)


def test_dsk_detects_generated_schema_mismatch(tmp_path: Path) -> None:
    gen = _load_generator()
    lines = gen.emit_events(_sample_events())
    first_event = json.loads(lines[0])
    first_event.pop("signature")
    lines[0] = gen.event_line(first_event)

    with pytest.raises(AuditChainCorrupt, match="missing signature field"):
        verify_audit_log(_write_audit_log(tmp_path, lines))


def test_emit_events_is_idempotent_for_same_input() -> None:
    gen = _load_generator()
    events = _sample_events()

    assert gen.emit_events(copy.deepcopy(events)) == gen.emit_events(copy.deepcopy(events))
