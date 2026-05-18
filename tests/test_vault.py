"""Tests for encrypted vault storage."""

import pytest

import pwcli.vault as vault


@pytest.fixture
def isolated_vault(tmp_path, monkeypatch):
    """Redirect vault storage to a temporary test directory."""
    vault_dir = tmp_path / "pwcli"
    vault_file = vault_dir / "vault.enc"

    monkeypatch.setattr(vault, "VAULT_DIR", vault_dir)
    monkeypatch.setattr(vault, "VAULT_FILE", vault_file)

    return vault_file


def test_load_vault_returns_empty_vault_when_file_missing(isolated_vault):
    data = vault.load_vault("test-master-password")

    assert data == {"entries": []}
    assert not isolated_vault.exists()


def test_add_get_list_and_delete_entry(isolated_vault):
    master_password = "test-master-password"

    vault.add_entry(master_password, "github", "secret-password")

    assert isolated_vault.exists()
    assert vault.get_entry(master_password, "github") == "secret-password"
    assert vault.list_entries(master_password) == ["github"]

    deleted = vault.delete_entry(master_password, "github")

    assert deleted is True
    assert vault.get_entry(master_password, "github") is None
    assert vault.list_entries(master_password) == []


def test_add_entry_replaces_existing_entry(isolated_vault):
    master_password = "test-master-password"

    vault.add_entry(master_password, "github", "old-password")
    vault.add_entry(master_password, "github", "new-password")

    assert vault.get_entry(master_password, "github") == "new-password"
    assert vault.list_entries(master_password) == ["github"]


def test_delete_missing_entry_returns_false(isolated_vault):
    master_password = "test-master-password"

    vault.add_entry(master_password, "github", "secret-password")

    deleted = vault.delete_entry(master_password, "missing")

    assert deleted is False
    assert vault.list_entries(master_password) == ["github"]


def test_wrong_master_password_fails(isolated_vault):
    vault.add_entry("correct-master-password", "github", "secret-password")

    with pytest.raises(ValueError, match="Invalid master password"):
        vault.get_entry("wrong-master-password", "github")


def test_vault_file_does_not_store_plaintext(isolated_vault):
    master_password = "test-master-password"
    entry_name = "github"
    entry_password = "secret-password"

    vault.add_entry(master_password, entry_name, entry_password)

    raw_file_content = isolated_vault.read_bytes()

    assert entry_name.encode() not in raw_file_content
    assert entry_password.encode() not in raw_file_content