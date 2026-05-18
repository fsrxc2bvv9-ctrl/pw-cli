from __future__ import annotations

import json

import typer
from rich.console import Console

from pwcli.clipboard import copy_to_clipboard
from pwcli.config import get_phrase_defaults
from pwcli.wordlists import generate_passphrase

console = Console()

app = typer.Typer(
    help="Generate memorable passphrases.",
    rich_help_panel="Commands",
)


@app.callback(invoke_without_command=True)
def phrase_root(
    ctx: typer.Context,
    words: int | None = typer.Option(None, "--words", "-w", help="Number of words"),
    separator: str | None = typer.Option(None, "--separator", "-s", help="Separator character"),
    capitalize: bool | None = typer.Option(
        None,
        "--capitalize",
        "-C",
        help="Capitalize first letter of each word",
    ),
    numbers: bool | None = typer.Option(
        None,
        "--numbers",
        "-n",
        help="Add 4-digit number at the end",
    ),
    count: int | None = typer.Option(
        None,
        "--count",
        "-c",
        help="Number of passphrases to generate",
        min=1,
    ),
    copy: bool = typer.Option(
        False,
        "--copy",
        help="Copy last passphrase to clipboard",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output in JSON format",
    ),
) -> None:
    """Generate memorable and secure passphrases using the EFF wordlist."""
    if ctx is not None and ctx.invoked_subcommand is not None:
        return

    defaults = get_phrase_defaults()

    words = words if words is not None else defaults["words"]
    separator = separator if separator is not None else defaults["separator"]
    capitalize = capitalize if capitalize is not None else defaults["capitalize"]
    numbers = numbers if numbers is not None else defaults["numbers"]
    count = count if count is not None else defaults.get("count", 1)

    passphrases = []
    for i in range(count):
        phrase = generate_passphrase(
            num_words=words,
            separator=separator,
            capitalize=capitalize,
            add_number=numbers,
        )
        passphrases.append(phrase)

        if not json_output:
            console.print(f"[bold green]Passphrase {i + 1}:[/] [white]{phrase}[/]")

    if json_output:
        print(json.dumps({"passphrases": passphrases}, ensure_ascii=False))

    if copy and passphrases:
        if copy_to_clipboard(passphrases[-1]):
            console.print("[dim]→ copied to clipboard (will be cleared in 30 seconds)[/]")
        else:
            console.print("[yellow]⚠️  Could not copy to clipboard[/]")
