"""Interface CLI pour AGENT_SECRET_ADL."""

import logging
import sys
from pathlib import Path

import pandas as pd
import typer
from rich.console import Console
from rich.table import Table

from agent_secret_adl.extraction import extract_admissibles_from_pdf
from agent_secret_adl.enrichment import enrich_with_hunter
from agent_secret_adl.enrichment.phones import enrich_with_phones

# Configuration
console = Console()
app = typer.Typer(
    name="agent-secret-adl",
    help="🚕 AGENT_SECRET_ADL - Extraction de candidats TAXIS/VTC",
)

# Logger
logger = logging.getLogger(__name__)


@app.command("extract-admissibles")
def extract_admissibles(
    pdf_path: str = typer.Option(
        ...,
        "--pdf-path",
        help="Chemin du fichier PDF à traiter",
        metavar="PATH",
    ),
    output_csv: str = typer.Option(
        ...,
        "--output-csv",
        help="Chemin du fichier CSV de sortie",
        metavar="PATH",
    ),
    departement: str = typer.Option(
        ...,
        "--departement",
        help="Code ou nom du département (ex: 78, Paris)",
        metavar="STR",
    ),
    session_date: str = typer.Option(
        ...,
        "--session-date",
        help="Date de la session (ex: 2025-02-25)",
        metavar="DATE",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Afficher les logs détaillés",
    ),
) -> None:
    """
    Extrait les candidats admissibles depuis un PDF.

    Exemples:
        python -m agent_secret_adl extract-admissibles \\
          --pdf-path data/admissibles.pdf \\
          --output-csv output/results.csv \\
          --departement 78 \\
          --session-date 2025-02-25
    """
    # Configuration du logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Afficher le header
    console.print()
    console.print(
        "[bold cyan]🚕 AGENT_SECRET_ADL - Extraction d'admissibles[/bold cyan]"
    )
    console.print()

    try:
        # Validation des chemins
        pdf_path_obj = Path(pdf_path)
        output_csv_obj = Path(output_csv)

        if not pdf_path_obj.exists():
            console.print(
                f"[bold red]❌ Erreur :[/bold red] Le fichier PDF n'existe pas"
            )
            console.print(f"   Chemin fourni : {pdf_path}")
            raise typer.Exit(code=1)

        # Afficher les paramètres
        console.print("[bold]Paramètres :[/bold]")
        console.print(f"  📄 PDF           : {pdf_path}")
        console.print(f"  💾 Sortie        : {output_csv}")
        console.print(f"  📍 Département   : {departement}")
        console.print(f"  📅 Session       : {session_date}")
        console.print()

        # Lancer l'extraction
        console.print("[bold]⏳ Extraction en cours...[/bold]")
        extract_admissibles_from_pdf(
            pdf_path=pdf_path,
            output_csv_path=output_csv,
            departement=departement,
            session_date=session_date,
        )

        # Charger et afficher les résultats
        df = pd.read_csv(output_csv)

        # Statistiques par catégorie
        stats_by_category = df["categorie"].value_counts().to_dict()

        console.print()
        console.print("[bold green]✅ Extraction réussie ![/bold green]")
        console.print()

        # Tableau de résumé
        table = Table(title="📊 Résumé d'extraction", show_header=True)
        table.add_column("Métrique", style="cyan", width=25)
        table.add_column("Valeur", style="green", width=20)

        table.add_row("Total candidats", str(len(df)))
        for category, count in sorted(stats_by_category.items()):
            table.add_row(f"  ↳ {category}", str(count))
        table.add_row("Fichier généré", str(output_csv))

        console.print(table)
        console.print()

        # Afficher un aperçu des données
        if len(df) > 0:
            console.print("[bold]📝 Aperçu des données (5 premiers enregistrements) :[/bold]")
            console.print()

            preview_table = Table(show_header=True, box=None)
            preview_table.add_column("Catégorie", style="cyan")
            preview_table.add_column("N° Candidat", style="yellow")
            preview_table.add_column("Prénom", style="blue")
            preview_table.add_column("NOM", style="blue")

            for _, row in df.head(5).iterrows():
                preview_table.add_row(
                    row["categorie"],
                    str(row["numero_candidat"]),
                    row["prenom"],
                    row["nom"],
                )

            console.print(preview_table)
            console.print()

        console.print(
            "[bold cyan]💡 Conseil :[/bold cyan] Consultez le fichier CSV complet "
            f"pour plus de détails : {output_csv}"
        )
        console.print()

    except FileNotFoundError as e:
        console.print(f"[bold red]❌ Erreur fichier :[/bold red] {e}")
        raise typer.Exit(code=1)

    except ValueError as e:
        console.print(f"[bold red]❌ Erreur validation :[/bold red] {e}")
        raise typer.Exit(code=1)

    except RuntimeError as e:
        console.print(f"[bold red]❌ Erreur traitement :[/bold red] {e}")
        raise typer.Exit(code=1)

    except Exception as e:
        console.print(f"[bold red]❌ Erreur inattendue :[/bold red] {e}")
        if verbose:
            console.print_exception()
        raise typer.Exit(code=1)


@app.command("info")
def info() -> None:
    """Affiche les informations du projet."""
    console.print()
    console.print("[bold cyan]ℹ️  AGENT_SECRET_ADL - Informations[/bold cyan]")
    console.print()

    from agent_secret_adl import __version__

    info_table = Table(show_header=False, box=None)
    info_table.add_row("[bold]Nom[/bold]", "AGENT_SECRET_ADL")
    info_table.add_row("[bold]Version[/bold]", __version__)
    info_table.add_row(
        "[bold]Description[/bold]",
        "Extraction et enrichissement de candidats TAXIS/VTC",
    )
    info_table.add_row("[bold]Modules[/bold]", "extraction, normalization, enrichment, reporting")

    console.print(info_table)
    console.print()


@app.command("enrich-hunter")
def enrich_hunter(
    input_csv: str = typer.Option(
        ...,
        "--input-csv",
        help="Chemin du CSV d'admissibles (sortie de extract-admissibles)",
        metavar="PATH",
    ),
    output_csv: str = typer.Option(
        ...,
        "--output-csv",
        help="Chemin du CSV enrichi",
        metavar="PATH",
    ),
    api_key: str = typer.Option(
        "sk_test_stub",
        "--api-key",
        help="Clé API Hunter.io (optionnel, utilise stub par défaut)",
        metavar="STR",
    ),
    max_rows: int = typer.Option(
        20,
        "--max-rows",
        help="Nombre maximum de candidats à enrichir (limitation API)",
        metavar="INT",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Afficher les logs détaillés",
    ),
) -> None:
    """
    Enrichit les candidats avec des emails (Hunter.io stub).

    Ajoute des colonnes email et métadonnées d'enrichissement.
    Actuellement un stub prêt pour intégration API.

    Exemples:
        python -m agent_secret_adl enrich-hunter \\
          --input-csv output/admissibles.csv \\
          --output-csv output/admissibles_enrichis.csv \\
          --max-rows 20
    """
    # Configuration du logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Afficher le header
    console.print()
    console.print(
        "[bold cyan]📧 AGENT_SECRET_ADL - Enrichissement Hunter[/bold cyan]"
    )
    console.print()

    try:
        # Validation des chemins
        input_csv_obj = Path(input_csv)

        if not input_csv_obj.exists():
            console.print(
                f"[bold red]❌ Erreur :[/bold red] Le fichier CSV n'existe pas"
            )
            console.print(f"   Chemin fourni : {input_csv}")
            raise typer.Exit(code=1)

        # Afficher les paramètres
        console.print("[bold]Paramètres :[/bold]")
        console.print(f"  📥 Entrée        : {input_csv}")
        console.print(f"  📤 Sortie        : {output_csv}")
        console.print(f"  🔑 API Key       : {'*' * 8}")
        console.print(f"  📊 Max lignes    : {max_rows}")
        console.print()

        # Lancer l'enrichissement
        console.print("[bold]⏳ Enrichissement en cours...[/bold]")
        enrich_with_hunter(
            input_csv_path=input_csv,
            output_csv_path=output_csv,
            api_key=api_key,
            max_rows=max_rows,
        )

        # Charger et afficher les résultats
        df = pd.read_csv(output_csv)

        console.print()
        console.print("[bold green]✅ Enrichissement réussi ![/bold green]")
        console.print()

        # Statistiques d'enrichissement
        enriched_count = (df["enrichment_status"] == "simulated").sum()
        skipped_count = (df["enrichment_status"] == "skipped").sum()
        error_count = (df["enrichment_status"] == "error").sum()

        # Tableau de résumé
        table = Table(title="📊 Résumé d'enrichissement", show_header=True)
        table.add_column("Métrique", style="cyan", width=25)
        table.add_column("Valeur", style="green", width=20)

        table.add_row("Total lignes", str(len(df)))
        table.add_row("Enrichis (simulé)", str(enriched_count))
        table.add_row("Non traités", str(skipped_count))
        if error_count > 0:
            table.add_row("Erreurs", str(error_count))
        table.add_row("Fichier généré", str(output_csv))

        console.print(table)
        console.print()

        # Afficher un aperçu
        if len(df) > 0:
            console.print(
                "[bold]📝 Aperçu des données enrichies (5 premiers) :[/bold]"
            )
            console.print()

            preview_table = Table(show_header=True, box=None)
            preview_table.add_column("Prénom", style="blue")
            preview_table.add_column("NOM", style="blue")
            preview_table.add_column("Email simulé", style="yellow")
            preview_table.add_column("Statut", style="cyan")

            for _, row in df.head(5).iterrows():
                email = row.get("email", "N/A")
                status = row.get("enrichment_status", "unknown")
                preview_table.add_row(
                    row["prenom"],
                    row["nom"],
                    str(email) if email else "N/A",
                    status,
                )

            console.print(preview_table)
            console.print()

        console.print(
            "[bold cyan]💡 Info :[/bold cyan] Enrichissement actuellement en mode "
            "stub (simulations). Prêt pour intégration Hunter.io réelle."
        )
        console.print()

    except FileNotFoundError as e:
        console.print(f"[bold red]❌ Erreur fichier :[/bold red] {e}")
        raise typer.Exit(code=1)

    except ValueError as e:
        console.print(f"[bold red]❌ Erreur validation :[/bold red] {e}")
        raise typer.Exit(code=1)

    except RuntimeError as e:
        console.print(f"[bold red]❌ Erreur traitement :[/bold red] {e}")
        raise typer.Exit(code=1)

    except Exception as e:
        console.print(f"[bold red]❌ Erreur inattendue :[/bold red] {e}")
        if verbose:
            console.print_exception()
        raise typer.Exit(code=1)


@app.command("enrich-phones")
def enrich_phones(
    input_csv: str = typer.Option(
        ...,
        "--input-csv",
        help="CSV d'entrée (sortie enrich-hunter recommandée)",
        metavar="PATH",
    ),
    output_csv: str = typer.Option(
        ...,
        "--output-csv",
        help="CSV enrichi avec téléphones",
        metavar="PATH",
    ),
    max_rows: int = typer.Option(
        50,
        "--max-rows",
        help="Nombre max de candidats à traiter (contrôle de charge)",
        metavar="INT",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Mode verbose (debug logs)",
    ),
) -> None:
    """🔍 Enrichit un CSV avec des téléphones via sources publiques gratuites.

    Sources multi-canaux (cascade) :
    - SIRENE (données officielles France)
    - Pages Jaunes publiques (annuaire gratuit)
    - Annuaires professionnels publics
    - Validation et normalisation format FR

    Idéal pour enrichir après 'enrich-hunter' (ajout emails).

    Exemple :
        agent-secret-adl enrich-phones \\
            --input-csv output/admissibles_emails.csv \\
            --output-csv output/admissibles_complete.csv \\
            --max-rows 50
    """
    # Configuration logging
    if verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    logger.debug(f"CLI enrich-phones appelée")
    logger.debug(f"  input_csv: {input_csv}")
    logger.debug(f"  output_csv: {output_csv}")
    logger.debug(f"  max_rows: {max_rows}")

    console.print(
        "[bold cyan]🚕 AGENT_SECRET_ADL - Enrichissement téléphones[/bold cyan]"
    )
    console.print()

    try:
        # Valider les paramètres
        if max_rows < 1:
            raise ValueError("max_rows doit être >= 1")

        input_path = Path(input_csv)
        if not input_path.exists():
            raise FileNotFoundError(f"Fichier {input_csv} non trouvé")

        if not input_path.suffix == ".csv":
            raise ValueError(f"Fichier doit être un CSV (trouvé: {input_path.suffix})")

        # Afficher les paramètres
        table = Table(title="📋 Paramètres d'enrichissement", show_header=True)
        table.add_column("Paramètre", style="cyan", width=20)
        table.add_column("Valeur", style="green")
        table.add_row("CSV d'entrée", input_csv)
        table.add_row("CSV de sortie", output_csv)
        table.add_row("Max lignes", str(max_rows))
        table.add_row("Sources", "SIRENE + Pages Jaunes + Annuaires")
        console.print(table)
        console.print()

        # Lancer l'enrichissement
        console.print(
            "[bold yellow]⏳ Traitement des candidats...[/bold yellow]"
        )
        enrich_with_phones(
            input_csv_path=input_csv,
            output_csv_path=output_csv,
            max_rows=max_rows,
        )
        console.print()

        # Afficher les stats
        df = pd.read_csv(output_csv)
        enriched_count = (df["phone_status"] == "found").sum()
        simulated_count = (df["phone_status"] == "simulated").sum()
        skipped_count = (df["phone_status"] == "skipped").sum()
        error_count = (df["phone_status"] == "error").sum()

        # Tableau de résumé
        table = Table(title="📊 Résumé d'enrichissement téléphones", show_header=True)
        table.add_column("Métrique", style="cyan", width=25)
        table.add_column("Valeur", style="green", width=20)

        table.add_row("Total lignes", str(len(df)))
        table.add_row("Téléphones trouvés (réels)", str(enriched_count))
        table.add_row("Téléphones simulés (stub)", str(simulated_count))
        table.add_row("Non traités", str(skipped_count))
        if error_count > 0:
            table.add_row("Erreurs", str(error_count))
        table.add_row("Fichier généré", str(output_csv))

        console.print(table)
        console.print()

        # Afficher un aperçu
        if len(df) > 0:
            console.print(
                "[bold]📝 Aperçu des données enrichies (5 premiers) :[/bold]"
            )
            console.print()

            preview_table = Table(show_header=True, box=None)
            preview_table.add_column("Prénom", style="blue")
            preview_table.add_column("NOM", style="blue")
            preview_table.add_column("Téléphone", style="yellow")
            preview_table.add_column("Source", style="magenta")
            preview_table.add_column("Statut", style="cyan")

            for _, row in df.head(5).iterrows():
                phone = row.get("phone", "N/A")
                source = row.get("phone_source", "unknown")
                status = row.get("phone_status", "unknown")
                preview_table.add_row(
                    row["prenom"],
                    row["nom"],
                    str(phone) if phone else "N/A",
                    str(source),
                    status,
                )

            console.print(preview_table)
            console.print()

        console.print(
            "[bold cyan]💡 Sources utilisées :[/bold cyan]\n"
            "  • SIRENE - Système officiel France (gratuit, fiable)\n"
            "  • Pages Jaunes - Annuaire public (gratuit, scraping ok)\n"
            "  • Annuaires publics - Open Data + local APIs\n"
            "  • Stub/Simulation - Pattern générés pour test\n"
        )
        console.print(
            "[bold yellow]ℹ️  En production :[/bold yellow] \n"
            "  Sources réelles intégrées. Tester avec --max-rows 5-10 en début."
        )
        console.print()

    except FileNotFoundError as e:
        console.print(f"[bold red]❌ Erreur fichier :[/bold red] {e}")
        raise typer.Exit(code=1)

    except ValueError as e:
        console.print(f"[bold red]❌ Erreur validation :[/bold red] {e}")
        raise typer.Exit(code=1)

    except RuntimeError as e:
        console.print(f"[bold red]❌ Erreur traitement :[/bold red] {e}")
        raise typer.Exit(code=1)

    except Exception as e:
        console.print(f"[bold red]❌ Erreur inattendue :[/bold red] {e}")
        if verbose:
            console.print_exception()
        raise typer.Exit(code=1)


def main() -> None:
    """Point d'entrée principal."""
    app()


if __name__ == "__main__":
    main()
