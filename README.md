# pw-cli

[![CI](https://github.com/fsrxc2bvv9-ctrl/pw-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/fsrxc2bvv9-ctrl/pw-cli/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org)

**Modern CLI Password Generator with an Encrypted Local Vault**

Fast, secure, local-first command-line tool for generating strong passwords, memorable passphrases, and storing credentials in an encrypted local vault.

## Features

- `pwcli` / `pwcli generate` / `pwcli gen` — strong random passwords
- `pwcli phrase` — memorable passphrases using the EFF wordlist
- `pwcli vault` — encrypted local password vault
- `pwcli config` — flexible TOML configuration
- `--copy` — copy to clipboard with automatic clearing after 30 seconds
- `--json` — machine-readable output
- Shell completion support

## Quick Start

```bash
# Generate password
pwcli generate -l 20 --copy

# Short alias
pwcli gen -l 32 --no-symbols --copy

# Memorable passphrase
pwcli phrase -w 6 -C -n --copy

# Vault
pwcli vault init
pwcli vault add github
pwcli vault get github --copy
```

## Shell Completion

```bash
pwcli --install-completion
```

Restart your terminal afterwards.

## Security Highlights

- Passwords are generated using Python's `secrets` module with configurable character classes
- Passphrases use the EFF wordlist
- `--copy` copies passwords to the clipboard and attempts to clear it after **30 seconds**
  - *Clipboard clearing is best-effort: if the process exits early or the terminal is closed, the clipboard may not be cleared*
- Vault data is encrypted locally using **Fernet encryption (AES-128-CBC + HMAC-SHA256)**
- Vault keys are derived from the master password using PBKDF2 with 480,000 iterations
- **Master password is never stored** — only a random salt and the encrypted vault data are written to disk
- No data is ever sent over the network

**Threat model:** `pw-cli` protects your vault if the vault file is copied or leaked without the master password. It does **not** protect against malware, keyloggers, compromised terminals, screen recording, clipboard monitoring, or a weak master password.

For highly sensitive accounts, consider using a professionally audited password manager.

## Installation from source

```bash
git clone https://github.com/fsrxc2bvv9-ctrl/pw-cli.git
cd pw-cli

# Recommended
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"

pwcli --help
```
## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

MIT
