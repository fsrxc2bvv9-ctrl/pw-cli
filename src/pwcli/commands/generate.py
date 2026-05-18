from __future__ import annotations

import json
import secrets
import string

import typer
from rich.console import Console

from pwcli.clipboard import copy_to_clipboard
from pwcli.config import get_generate_defaults

console = Console()

AMBIGUOUS_CHARS = "0O1lI"


def generate(
    length: int | None = typer.Option(None, "--length", "-l", min=4),
    count: int | None = typer.Option(None, "--count", "-c", min=1),
    uppercase: bool | None = typer.Option(None, "--uppercase/--no-uppercase"),
    lowercase: bool | None = typer.Option(None, "--lowercase/--no-lowercase"),
    digits: bool | None = typer.Option(None, "--digits/--no-digits"),
    symbols: bool | None = typer.Option(None, "--symbols/--no-symbols"),
    exclude_ambiguous: bool | None = typer.Option(
        None,
        "--exclude-ambiguous/--no-exclude-ambiguous",
        help="Exclude visually ambiguous characters: 0 O 1 l I",
    ),
    copy: bool = typer.Option(False, "--copy"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    defaults = get_generate_defaults()

    length = length if length is not None else defaults["length"]
    count = count if count is not None else defaults["count"]
    uppercase = uppercase if uppercase is not None else defaults["uppercase"]
    lowercase = lowercase if lowercase is not None else defaults["lowercase"]
    digits = digits if digits is not None else defaults["digits"]
    symbols = symbols if symbols is not None else defaults["symbols"]
    exclude_ambiguous = (
        exclude_ambiguous
        if exclude_ambiguous is not None
        else defaults["exclude_ambiguous"]
    )

    passwords = [
        generate_password(
            length=length,
            uppercase=uppercase,
            lowercase=lowercase,
            digits=digits,
            symbols=symbols,
            exclude_ambiguous=exclude_ambiguous,
        )
        for _ in range(count)
    ]

    if json_output:
        print(json.dumps({"passwords": passwords}, ensure_ascii=False))
    else:
        for i, password in enumerate(passwords, start=1):
            console.print(f"[bold green]Password {i}:[/] {password}")

    if copy and passwords:
        if copy_to_clipboard(passwords[-1]):
            console.print("[dim]→ copied to clipboard (will be cleared in 30 seconds)[/]")
        else:
            console.print("[yellow]⚠️  Could not copy to clipboard[/]")


def generate_password(
    length: int = 16,
    uppercase: bool = True,
    lowercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
    exclude_ambiguous: bool = False,
) -> str:
    if length < 4:
        raise ValueError("Password length must be at least 4")

    raw_pools: list[str] = []

    if uppercase:
        raw_pools.append(string.ascii_uppercase)
    if lowercase:
        raw_pools.append(string.ascii_lowercase)
    if digits:
        raw_pools.append(string.digits)
    if symbols:
        raw_pools.append(string.punctuation)

    if not raw_pools:
        raise ValueError("At least one character category must be enabled")

    pools = []
    for pool in raw_pools:
        if exclude_ambiguous:
            pool = "".join(ch for ch in pool if ch not in AMBIGUOUS_CHARS)
        if pool:
            pools.append(pool)

    if not pools:
        raise ValueError("No characters available for password generation")

    if length < len(pools):
        raise ValueError(
            f"Password length must be at least {len(pools)} "
            "to include every enabled character category"
        )

    required_chars = [secrets.choice(pool) for pool in pools]
    all_chars = "".join(pools)
    remaining_chars = [secrets.choice(all_chars) for _ in range(length - len(required_chars))]

    password_chars = required_chars + remaining_chars
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)
