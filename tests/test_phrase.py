"""Tests for passphrase generation."""

import pytest

from pwcli.wordlists import generate_passphrase


def test_generate_passphrase_default_word_count():
    phrase = generate_passphrase()

    parts = phrase.split("-")

    assert len(parts) == 5
    assert all(parts)


def test_generate_passphrase_custom_word_count():
    phrase = generate_passphrase(num_words=7)

    parts = phrase.split("-")

    assert len(parts) == 7
    assert all(parts)


def test_generate_passphrase_custom_separator():
    phrase = generate_passphrase(num_words=4, separator="_")

    parts = phrase.split("_")

    assert len(parts) == 4
    assert "-" not in phrase


def test_generate_passphrase_capitalize():
    phrase = generate_passphrase(num_words=4, capitalize=True)

    parts = phrase.split("-")

    assert len(parts) == 4
    assert all(word[0].isupper() for word in parts)


def test_generate_passphrase_add_number():
    phrase = generate_passphrase(num_words=4, add_number=True)

    parts = phrase.split("-")

    assert len(parts) == 5
    assert parts[-1].isdigit()
    assert len(parts[-1]) == 4


def test_generate_passphrase_rejects_zero_words():
    with pytest.raises(ValueError, match="at least 1"):
        generate_passphrase(num_words=0)