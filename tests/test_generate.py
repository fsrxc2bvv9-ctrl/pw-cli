"""Basic tests for the password generator."""

import string

import pytest

from pwcli.commands.generate import generate_password


class TestGeneratePassword:
    def test_default_length(self):
        pwd = generate_password()
        assert len(pwd) == 16

    def test_custom_length(self):
        pwd = generate_password(length=32)
        assert len(pwd) == 32

    def test_minimum_length(self):
        with pytest.raises(ValueError, match="at least 4"):
            generate_password(length=3)

    def test_only_digits(self):
        pwd = generate_password(
            length=20,
            uppercase=False,
            lowercase=False,
            digits=True,
            symbols=False,
        )
        assert all(c in string.digits for c in pwd)
        assert len(pwd) == 20

    def test_excludes_ambiguous_chars(self):
        ambiguous = "0O1lI"
        pwd = generate_password(length=30, exclude_ambiguous=True)
        assert not any(ch in ambiguous for ch in pwd)

    def test_all_categories_disabled_raises(self):
        with pytest.raises(ValueError, match="At least one character category"):
            generate_password(
                length=10,
                uppercase=False,
                lowercase=False,
                digits=False,
                symbols=False,
            )

    def test_generates_different_passwords(self):
        pwds = {generate_password(length=12) for _ in range(5)}
        assert len(pwds) == 5  # extremely unlikely collision

    def test_contains_at_least_one_of_each_enabled_category(self):
        pwd = generate_password(
            length=12,
            uppercase=True,
            lowercase=True,
            digits=True,
            symbols=True,
        )
        has_upper = any(c.isupper() for c in pwd)
        has_lower = any(c.islower() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_symbol = any(c in string.punctuation for c in pwd)

        assert has_upper and has_lower and has_digit and has_symbol