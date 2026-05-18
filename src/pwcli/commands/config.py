import typer
from rich.console import Console
from rich.table import Table

from pwcli.config import load_config, set_config_value

console = Console()

app = typer.Typer(help="Manage pw-cli configuration", rich_help_panel="Commands")


@app.command("show")
def config_show(
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
) -> None:
    """Show current configuration."""
    cfg = load_config()

    if json_output:
        import json
        print(json.dumps(cfg, ensure_ascii=False, indent=2))
        return

    console.print("[bold cyan]pw-cli Configuration[/]\n")

    # Generate section
    table = Table(title="Generate", title_style="bold green")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="white")
    for k, v in cfg["generate"].items():
        table.add_row(k, str(v))
    console.print(table)

    # Phrase section
    table = Table(title="Phrase", title_style="bold green")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="white")
    for k, v in cfg["phrase"].items():
        table.add_row(k, str(v))
    console.print(table)


@app.command("set")
def config_set(
    key: str = typer.Argument(..., help="Key (e.g. generate.length or phrase.words)"),
    value: str = typer.Argument(..., help="New value"),
) -> None:
    """Change a configuration value."""
    # Auto-convert types
    if value.lower() in ("true", "1", "yes", "on"):
        value = True
    elif value.lower() in ("false", "0", "no", "off"):
        value = False
    elif value.isdigit():
        value = int(value)

    set_config_value(key, value)
    console.print(f"[bold green]✅ {key} = {value}[/]")