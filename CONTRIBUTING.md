# Contributing

This repo is a small integration fixture for keeperCMD -> DSK rehearsal.

## Development setup

```bash
git clone https://github.com/msawczynk/dsk-keepercmd-demo.git
cd dsk-keepercmd-demo
pip install -e /path/to/dsk
```

## Local validation

```bash
make demo-clean demo-all
```

The run-dir fixture must remain synthetic or anonymized. Do not commit real
Keeper tenant data, credentials, KSM config, tokens, or private keys.

## Pull requests

- Keep fixture changes small and explain the keeperCMD contract behavior being
  exercised.
- Update `CHANGELOG.md` when changing demo behavior.
- Link any DSK or keeperCMD contract issue that motivated the change.
- For vulnerabilities, follow [`SECURITY.md`](SECURITY.md) rather than opening
  a public issue.
