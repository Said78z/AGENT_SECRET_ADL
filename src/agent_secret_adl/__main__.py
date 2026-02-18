"""Point d'entrée CLI pour AGENT_SECRET_ADL."""

import typer
from pathlib import Path

app = typer.Typer(help="AGENT_SECRET_ADL - Extraction et enrichissement de candidatures TAXIS/VTC")


@app.command()
def extract(
    pdf_path: str = typer.Argument(..., help="Chemin du fichier PDF à traiter"),
    output: str = typer.Option("output.csv", help="Chemin du fichier CSV de sortie"),
    enrich: bool = typer.Option(False, help="Activer l'enrichissement optionnel"),
) -> None:
    """Extrait les candidats depuis un PDF et exporte en CSV."""
    typer.echo(f"📄 Extraction depuis : {pdf_path}")
    typer.echo(f"💾 Export vers : {output}")
    typer.echo(f"➕ Enrichissement : {'Activé' if enrich else 'Désactivé'}")
    typer.echo("✅ Fonctionnalité à implémenter")


@app.command()
def validate(
    csv_path: str = typer.Argument(..., help="Chemin du fichier CSV à valider"),
) -> None:
    """Valide un fichier CSV de candidats."""
    typer.echo(f"🔍 Validation : {csv_path}")
    typer.echo("✅ Fonctionnalité à implémenter")


@app.command()
def config() -> None:
    """Affiche la configuration actuelle."""
    from agent_secret_adl import config as cfg

    typer.echo("⚙️  Configuration de AGENT_SECRET_ADL")
    typer.echo(f"Version: {cfg.__file__}")
    typer.echo("✅ Fonctionnalité à implémenter")


if __name__ == "__main__":
    app()
