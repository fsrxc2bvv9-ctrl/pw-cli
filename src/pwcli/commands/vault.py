import getpass

import typer
from rich.console import Console
from rich.table import Table

from pwcli.vault import (
    VAULT_FILE,
    add_entry,
    delete_entry,
    get_entry,
    list_entries,
)

console = Console()

app = typer.Typer(help="Manage your encrypted password vault", rich_help_panel="Commands")


def _ask_master_password() -> str:
    return getpass.getpass("🔑 Master password: ")


def _ensure_vault_initialized() -> None:
    """Check if vault exists. If not — show friendly message."""
    if not VAULT_FILE.exists():
        console.print("[bold yellow]⚠️  Vault has not been initialized yet.[/]")
        console.print("To use the vault, you first need to create it.")
        console.print("\nRun the following command:\n")
        console.print("   [bold green]pwcli vault init[/]\n")
        raise typer.Exit(code=1)


@app.command("init")
def vault_init() -> None:
    """Initialize the password vault (first time setup)."""
    if VAULT_FILE.exists():
        console.print("[yellow]⚠️  Vault is already initialized.[/]")
        return

    console.print("[bold red]⚠️  IMPORTANT![/]")
    console.print("The master password is the only key to your vault.")
    console.print("If you forget it, [bold red]all passwords will be lost forever.[/]")
    console.print("Use a long and strong master password.\n")

    while True:
        mp1 = getpass.getpass("Create master password: ")
        mp2 = getpass.getpass("Repeat master password: ")
        if mp1 == mp2 and len(mp1) >= 8:
            break
        console.print("[red]Passwords do not match or are too short. Try again.[/]")


    from pwcli.vault import save_vault
    save_vault({"entries": []}, mp1)
    console.print("[bold green]✅ Vault created and encrypted successfully![/]")


@app.command("add")
def vault_add(
    name: str = typer.Argument(..., help="Name of the entry (e.g. github, gmail)"),
    password: str | None = typer.Option(
    None,
    "--password",
    "-p",
    help="Password to store. If omitted, a password will be generated.",
),
    length: int = typer.Option(24, "--length", "-l", help="Length of generated password"),
) -> None:
    """Add or update an entry in the vault."""
    _ensure_vault_initialized()
    mp = _ask_master_password()

    if password is None:
        from pwcli.commands.generate import generate_password
        password = generate_password(length=length)

    add_entry(mp, name, password)
    console.print(f"[bold green]✅ Entry '{name}' added/updated[/]")


@app.command("get")
def vault_get(
    name: str = typer.Argument(..., help="Name of the entry"),
    copy: bool = typer.Option(False, "--copy", help="Copy password to clipboard"),
) -> None:
    """Retrieve password by name."""
    _ensure_vault_initialized()
    mp = _ask_master_password()
    password = get_entry(mp, name)
    if password is None:
        console.print(f"[red]❌ Entry '{name}' not found[/]")
        return

    console.print(f"[bold green]🔑 {name}:[/] [white]{password}[/]")
    if copy:
        try:
            import pyperclip
            pyperclip.copy(password)
            console.print("[dim]→ copied to clipboard[/]")
        except Exception:
            console.print("[yellow]⚠️  Could not copy to clipboard[/]")


@app.command("list")
def vault_list() -> None:
    """List all entries in the vault."""
    _ensure_vault_initialized()
    mp = _ask_master_password()
    names = list_entries(mp)
    if not names:
        console.print("[yellow]Vault is empty.[/]")
        return

    table = Table(title="Your Vault")
    table.add_column("Name", style="cyan")
    for name in names:
        table.add_row(name)
    console.print(table)


@app.command("delete")
def vault_delete(name: str = typer.Argument(..., help="Name of the entry to delete")) -> None:
    """Delete an entry from the vault."""
    _ensure_vault_initialized()
    mp = _ask_master_password()
    if delete_entry(mp, name):
        console.print(f"[bold green]✅ Entry '{name}' deleted[/]")
    else:
        console.print(f"[red]❌ Entry '{name}' not found[/]")