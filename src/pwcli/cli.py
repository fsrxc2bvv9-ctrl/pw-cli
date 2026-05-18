from __future__ import annotations
import typer

from pwcli.commands.config import app as config_app
from pwcli.commands.generate import generate
from pwcli.commands.phrase import app as phrase_app
from pwcli.commands.vault import app as vault_app

app = typer.Typer()

# generate — ОДНА команда
app.command("generate")(generate)
app.command("gen")(generate)

# остальные — группы
app.add_typer(phrase_app, name="phrase")
app.add_typer(vault_app, name="vault")
app.add_typer(config_app, name="config")

if __name__ == "__main__":
    app()
