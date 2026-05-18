from __future__ import annotations

import secrets
from importlib.resources import files


def load_eff_wordlist() -> list[str]:
    """Load the EFF large wordlist."""
    wordlist_path = files("pwcli.data").joinpath("eff_large_wordlist.txt")
    content = wordlist_path.read_text(encoding="utf-8")

    words: list[str] = []

    for line in content.splitlines():
        line = line.strip()

        if not line:
            continue

        parts = line.split()

        if len(parts) >= 2:
            words.append(parts[1])

    if not words:
        raise RuntimeError("EFF wordlist is empty or could not be loaded")

    return words


_EFF_WORDS: list[str] | None = None


def get_wordlist() -> list[str]:
    """Return the cached EFF wordlist."""
    global _EFF_WORDS

    if _EFF_WORDS is None:
        _EFF_WORDS = load_eff_wordlist()

    return _EFF_WORDS


def generate_passphrase(
    num_words: int = 5,
    separator: str = "-",
    capitalize: bool = False,
    add_number: bool = False,
) -> str:
    """Generate a passphrase from the EFF wordlist."""
    if num_words < 1:
        raise ValueError("Number of words must be at least 1")

    wordlist = get_wordlist()
    selected = [secrets.choice(wordlist) for _ in range(num_words)]

    if capitalize:
        selected = [word.capitalize() for word in selected]

    passphrase = separator.join(selected)

    if add_number:
        passphrase = f"{passphrase}{separator}{secrets.randbelow(10_000):04d}"

    return passphrase