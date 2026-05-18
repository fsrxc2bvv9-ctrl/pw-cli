# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-05-18

### Added

- Strong random password generation with configurable length and character classes.
- Short alias command: `pwcli gen`.
- Memorable passphrase generation using the EFF large wordlist.
- Encrypted local vault for storing and retrieving password entries.
- TOML-based configuration management.
- Clipboard copy support with best-effort automatic clearing after 30 seconds.
- JSON output mode for scripting and automation.
- Shell completion support through Typer.
- GitHub Actions CI for Python 3.10, 3.11, 3.12, and 3.13.
- Tests for password generation, passphrase generation, and vault behavior.

### Security

- Vault encryption uses Fernet encryption.
- Vault keys are derived from the master password using PBKDF2-HMAC-SHA256 with 480,000 iterations.
- Master password is never stored.
- Vault file stores only encrypted data and a random salt.