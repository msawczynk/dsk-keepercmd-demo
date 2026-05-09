# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this repository, please report it responsibly:

1. **Do NOT open a public GitHub issue** for security vulnerabilities.
2. Email the maintainer directly: msawczynk@users.noreply.github.com
3. Provide a clear description of the issue, steps to reproduce, and (if applicable) suggested mitigation.
4. Allow up to 7 days for an initial response.

For verified vulnerabilities, expect:
- Acknowledgment within 7 days
- Coordinated disclosure timeline (typically 30-90 days from initial report)
- Credit in the fix commit / release notes (with your permission)

## Supported Versions

This project follows semantic versioning. Security fixes are backported to:
- Latest minor release of the current major version
- Latest minor release of the previous major version (until 6 months after a new major lands)

## Scope

In scope:
- Code in this repository
- Dependencies pinned in `pyproject.toml` / `requirements*.txt`

Out of scope (please report to the appropriate vendor):
- Vulnerabilities in Keeper Commander -> security@keepersecurity.com
- Vulnerabilities in third-party MCP clients
- Social engineering attacks unrelated to the codebase
