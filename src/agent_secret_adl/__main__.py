"""Point d'entrée CLI pour AGENT_SECRET_ADL."""

import logging
import typer
from pathlib import Path

from agent_secret_adl.extraction import extract_admissibles_from_pdf

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = typer.Typer(
    help="AGENT_SECRET_ADL - Extraction et enrichissement de candidatures TAXIS/VTC"
)


@app.command()
def extract(
    pdf_path: str = typer.Argument(..., help="Chemin du fichier PDF à traiter"),
    output: str = typer.Option(
        "output.csv", help="Chemin du fichier CSV de sortie"
    ),
    departement: str = typer.Option(
        ..., help="Code ou nom du département (ex: 75, Paris)"
    ),
    session_date: str = typer.Option(
        ..., help="Date de la session (ex: 2024-01-15)"
    ),
    enrich: bool = typer.Option(
        False, help="Activer l'enrichissement optionnel"
    ),
) -> None:
    """Extrait les candidats admissibles depuis un PDF et exporte en CSV."""
    try:
        typer.echo(f"📄 Extraction depuis : {pdf_path}")
        typer.echo(f"💾 Export vers : {output}")
        typer.echo(f"📍 Département : {departement}")
        typer.echo(f"📅 Session : {session_date}")
        typer.echo(f"➕ Enrichissement : {'Activé' if enrich else 'Désactivé'}")
        typer.echo("")

        extract_admissibles_from_pdf(
            pdf_path=pdf_path,
            output_csv_path=output,
            departement=departement,
            session_date=session_date,
        )

        typer.secho("✅ Extraction réussie !", fg=typer.colors.GREEN, bold=True)

    except FileNotFoundError as e:
        typer.secho(f"❌ Erreur : {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except ValueError as e:
        typer.secho(f"❌ Erreur : {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"❌ Erreur inattendue : {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


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
