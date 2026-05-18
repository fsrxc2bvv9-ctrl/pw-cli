from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import Any

import platformdirs
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

VAULT_DIR = Path(platformdirs.user_config_dir("pwcli"))
VAULT_FILE = VAULT_DIR / "vault.enc"

PBKDF2_ITERATIONS = 480_000
SALT_SIZE = 16


def _derive_key(master_password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from the master password and salt."""
    if not master_password:
        raise ValueError("Master password cannot be empty")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode("utf-8")))


def _encrypt(data: dict[str, Any], master_password: str) -> bytes:
    salt = os.urandom(SALT_SIZE)
    key = _derive_key(master_password, salt)
    encrypted_blob = Fernet(key).encrypt(json.dumps(data).encode("utf-8"))

    payload = {
        "version": 1,
        "kdf": "PBKDF2HMAC-SHA256",
        "iterations": PBKDF2_ITERATIONS,
        "salt": base64.urlsafe_b64encode(salt).decode("ascii"),
        "data": encrypted_blob.decode("ascii"),
    }

    return json.dumps(payload).encode("utf-8")


def _decrypt(encrypted: bytes, master_password: str) -> dict[str, Any]:
    try:
        payload = json.loads(encrypted.decode("utf-8"))
        salt = base64.urlsafe_b64decode(payload["salt"].encode("ascii"))
        encrypted_blob = payload["data"].encode("ascii")
    except (KeyError, json.JSONDecodeError, UnicodeDecodeError, TypeError) as exc:
        raise ValueError("Invalid vault file format") from exc

    key = _derive_key(master_password, salt)

    try:
        decrypted = Fernet(key).decrypt(encrypted_blob)
    except InvalidToken as exc:
        raise ValueError("Invalid master password") from exc

    return json.loads(decrypted.decode("utf-8"))


def load_vault(master_password: str) -> dict[str, Any]:
    """Load the vault or return an empty vault if it does not exist."""
    if not VAULT_FILE.exists():
        return {"entries": []}

    encrypted = VAULT_FILE.read_bytes()
    return _decrypt(encrypted, master_password)


def save_vault(data: dict[str, Any], master_password: str) -> None:
    """Encrypt and save the vault."""
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    encrypted = _encrypt(data, master_password)
    VAULT_FILE.write_bytes(encrypted)


def add_entry(master_password: str, name: str, password: str) -> None:
    data = load_vault(master_password)
    data["entries"] = [entry for entry in data["entries"] if entry["name"] != name]
    data["entries"].append({"name": name, "password": password})
    save_vault(data, master_password)


def get_entry(master_password: str, name: str) -> str | None:
    data = load_vault(master_password)

    for entry in data["entries"]:
        if entry["name"] == name:
            return str(entry["password"])

    return None


def list_entries(master_password: str) -> list[str]:
    data = load_vault(master_password)
    return [str(entry["name"]) for entry in data["entries"]]


def delete_entry(master_password: str, name: str) -> bool:
    data = load_vault(master_password)
    original_len = len(data["entries"])

    data["entries"] = [entry for entry in data["entries"] if entry["name"] != name]

    if len(data["entries"]) == original_len:
        return False

    save_vault(data, master_password)
    return True