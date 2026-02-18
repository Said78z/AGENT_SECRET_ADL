"""Module d'enrichissement avec intégration Hunter.io (stub pour l'instant)."""

import logging
from pathlib import Path
from typing import Optional
import re

import pandas as pd

logger = logging.getLogger(__name__)


def enrich_with_hunter(
    input_csv_path: str,
    output_csv_path: str,
    api_key: str,
    max_rows: int = 20,
) -> None:
    """
    Enrichit un CSV d'admissibles avec des emails via Hunter.io (stub).

    Charge le CSV source, applique un enrichissement simulé (structure prête
    pour intégration future d'une API email finder), et exporte le résultat.

    Args:
        input_csv_path: Chemin du CSV d'admissibles à enrichir.
        output_csv_path: Chemin de destination pour le CSV enrichi.
        api_key: Clé API Hunter.io (utilisée après implémentation réelle).
        max_rows: Nombre maximum de lignes à traiter (limiter l'usage API).

    Returns:
        None. Écrit directement le fichier CSV enrichi.

    Raises:
        FileNotFoundError: Si le fichier d'entrée n'existe pas.
        ValueError: Si le CSV est vide ou mal formé.

    Example:
        >>> enrich_with_hunter(
        ...     input_csv_path="output/admissibles.csv",
        ...     output_csv_path="output/admissibles_enrichis.csv",
        ...     api_key="pk_xxxxx",
        ...     max_rows=20,
        ... )

    Note:
        Actuellement un stub qui simule l'enrichissement.
        La vraie intégration Hunter.io sera branchée ultérieurement.
    """
    input_csv_path = Path(input_csv_path)
    output_csv_path = Path(output_csv_path)

    # Validation du fichier d'entrée
    if not input_csv_path.exists():
        logger.error(f"Fichier CSV non trouvé : {input_csv_path}")
        raise FileNotFoundError(f"Le fichier CSV n'existe pas : {input_csv_path}")

    logger.info(f"Début enrichissement : {input_csv_path}")
    logger.info(f"Limite : {max_rows} lignes")

    try:
        # Charger le CSV
        df = pd.read_csv(input_csv_path)

        if df.empty:
            logger.warning("Fichier CSV vide")
            raise ValueError("Le fichier CSV est vide")

        logger.info(f"Total lignes chargées : {len(df)}")

        # Limiter au nombre de lignes demandé
        df_to_enrich = df.head(max_rows).copy()

        logger.info(f"Traitement de {len(df_to_enrich)} lignes")

        # Appliquer l'enrichissement (stub)
        df_enriched = _enrich_candidates_stub(df_to_enrich, api_key)

        # Concaténer les lignes non traitées
        if len(df) > max_rows:
            df_remaining = df.iloc[max_rows:].copy()
            df_remaining["email"] = None
            df_remaining["enrichment_source"] = "not_processed"
            df_remaining["enrichment_status"] = "skipped"
            df_enriched = pd.concat(
                [df_enriched, df_remaining], ignore_index=True
            )

            logger.info(
                f"{len(df_remaining)} lignes non traitées (dépassement limite)"
            )

        # Créer le répertoire de sortie
        output_csv_path.parent.mkdir(parents=True, exist_ok=True)

        # Sauvegarder le CSV enrichi
        df_enriched.to_csv(output_csv_path, index=False, encoding="utf-8")

        logger.info(f"✅ Fichier enrichi généré : {output_csv_path}")
        logger.info(f"   {len(df_enriched)} candidats exportés")
        logger.info(
            f"   Enrichis : {(df_enriched['enrichment_status'] == 'simulated').sum()}"
        )

    except FileNotFoundError:
        raise
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'enrichissement : {e}")
        raise RuntimeError(f"Erreur lors de l'enrichissement : {e}") from e


def _enrich_candidates_stub(
    df: pd.DataFrame, api_key: str
) -> pd.DataFrame:
    """
    Enrichit les candidats avec un pattern d'email (stub).

    Simule l'enrichissement en générant des emails au format prenom.nom@example.com.
    Structure prête pour remplacer par un vrai appel Hunter.io.

    Args:
        df: DataFrame contenant les candidats (doit avoir 'prenom' et 'nom').
        api_key: Clé API (non utilisée pour l'instant, sera utilisée après).

    Returns:
        DataFrame enrichi avec colonnes email, enrichment_source, enrichment_status.
    """
    df_enriched = df.copy()

    # Initialiser les colonnes d'enrichissement
    df_enriched["email"] = None
    df_enriched["enrichment_source"] = "stub"
    df_enriched["enrichment_status"] = "simulated"

    # Générer les emails (stub pattern)
    for idx, row in df_enriched.iterrows():
        try:
            email = _generate_email_pattern(row["prenom"], row["nom"])
            df_enriched.at[idx, "email"] = email
        except (KeyError, TypeError) as e:
            logger.warning(f"Impossible de générer email pour ligne {idx} : {e}")
            df_enriched.at[idx, "enrichment_status"] = "error"

    logger.debug(
        f"Stub enrichissement : {(df_enriched['email'].notna()).sum()} emails générés"
    )

    return df_enriched


def _generate_email_pattern(prenom: str, nom: str) -> str:
    """
    Génère un email au format prenom.nom@example.com.

    Simule ce que Hunter.io retournerait.

    Args:
        prenom: Prénom du candidat.
        nom: Nom de famille du candidat.

    Returns:
        Email simulé (format stub).
    """
    if not prenom or not nom:
        raise ValueError("Prénom et nom requis")

    # Normaliser les caractères
    prenom_clean = re.sub(r"[^a-z0-9]", "", prenom.lower())
    nom_clean = re.sub(r"[^a-z0-9]", "", nom.lower())

    # Format : prenom.nom@example.com
    email = f"{prenom_clean}.{nom_clean}+test@example.com"

    return email


def is_enrichment_enabled() -> bool:
    """Vérifie si l'enrichissement est disponible."""
    return True


__all__ = ["enrich_with_hunter"]
