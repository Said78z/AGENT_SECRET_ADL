"""Extraction des candidats admissibles depuis PDF."""

import logging
import re
from pathlib import Path
from typing import Optional, List, Dict, Any

import pandas as pd
import pdfplumber

# Configuration du logger
logger = logging.getLogger(__name__)


def extract_admissibles_from_pdf(
    pdf_path: str,
    output_csv_path: str,
    departement: str,
    session_date: str,
) -> None:
    """
    Extrait les candidats admissibles depuis un PDF et exporte en CSV.

    Parse le texte du PDF (structure : Catégorie, N° candidat, Prénom, NOM, DECISION),
    filtre sur ADMISSIBLE, ajoute les métadonnées et sauvegarde en CSV.

    Args:
        pdf_path: Chemin vers le fichier PDF source.
        output_csv_path: Chemin de destination pour le fichier CSV.
        departement: Code ou nom du département (ex: "75", "Paris").
        session_date: Date de la session (ex: "2024-01-15").

    Returns:
        None. Écrit directement le fichier CSV.

    Raises:
        FileNotFoundError: Si le PDF n'existe pas.
        ValueError: Si aucune donnée pertinente n'est trouvée dans le PDF.

    Example:
        >>> extract_admissibles_from_pdf(
        ...     pdf_path="candidates.pdf",
        ...     output_csv_path="admissibles.csv",
        ...     departement="75",
        ...     session_date="2024-01-15",
        ... )
    """
    pdf_path = Path(pdf_path)
    output_csv_path = Path(output_csv_path)

    # Validation du fichier d'entrée
    if not pdf_path.exists():
        logger.error(f"Fichier PDF non trouvé : {pdf_path}")
        raise FileNotFoundError(f"Le fichier PDF n'existe pas : {pdf_path}")

    if not pdf_path.suffix.lower() == ".pdf":
        logger.error(f"Le fichier n'est pas un PDF : {pdf_path}")
        raise ValueError(f"Le fichier doit être un PDF : {pdf_path}")

    logger.info(
        f"Début extraction : {pdf_path} (département: {departement}, "
        f"session: {session_date})"
    )

    try:
        # Extraire le texte de toutes les pages
        all_data = _extract_candidates_from_pdf(pdf_path)

        if not all_data:
            logger.warning(f"Aucun candidat trouvé dans le PDF : {pdf_path}")
            raise ValueError("Aucune donnée à traiter trouvée dans le PDF")

        # Créer un DataFrame à partir des données extraites
        df = pd.DataFrame(all_data)

        logger.info(f"Total candidats extraits : {len(df)}")

        # Filtre : seuls les candidats admissibles
        df_admissibles = df[
            df["decision"].astype(str).str.upper() == "ADMISSIBLE"
        ].copy()

        if df_admissibles.empty:
            logger.warning(
                "Aucun candidat admissible trouvé dans le PDF"
            )
            raise ValueError("Aucun candidat admissible trouvé")

        logger.info(f"Candidats admissibles trouvés : {len(df_admissibles)}")

        # Ajouter les colonnes de métadonnées
        df_admissibles["departement"] = departement
        df_admissibles["session_date"] = session_date

        # S'assurer que le répertoire de sortie existe
        output_csv_path.parent.mkdir(parents=True, exist_ok=True)

        # Sauvegarder en CSV
        df_admissibles.to_csv(output_csv_path, index=False, encoding="utf-8")

        logger.info(f"✅ Fichier CSV généré : {output_csv_path}")
        logger.info(f"   {len(df_admissibles)} candidats admissibles exportés")

    except FileNotFoundError:
        raise
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Erreur inattendue lors de l'extraction : {e}")
        raise RuntimeError(f"Erreur inattendue : {e}") from e


def _extract_candidates_from_pdf(pdf_path: Path) -> List[Dict[str, Any]]:
    """
    Extrait tous les candidats du PDF en parsant le texte.

    Structure attendue :
        Catégorie N° candidat Prénom NOM DECISION

    Args:
        pdf_path: Chemin du fichier PDF.

    Returns:
        Liste de dictionnaires contenant les candidats.
    """
    all_data = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            logger.info(f"Nombre de pages : {total_pages}")

            for page_num, page in enumerate(pdf.pages, start=1):
                try:
                    text = page.extract_text()
                    if text:
                        candidates = _parse_text_to_candidates(text)
                        all_data.extend(candidates)
                        logger.debug(
                            f"Page {page_num} : {len(candidates)} candidats extraits"
                        )
                except Exception as e:
                    logger.warning(f"Erreur extraction page {page_num} : {e}")
                    continue

    except Exception as e:
        logger.error(f"Erreur lors de l'ouverture du PDF : {e}")
        raise

    return all_data


def _parse_text_to_candidates(text: str) -> List[Dict[str, Any]]:
    """
    Parse le texte brut du PDF pour extraire les candidats.

    Chaque ligne candidat suit le pattern :
        [Catégorie] N° Prénom NOM DECISION

    Args:
        text: Texte brut extrait d'une page PDF.

    Returns:
        Liste de dictionnaires candidats.
    """
    candidates = []
    lines = text.split("\n")

    current_category = None

    for line in lines:
        line = line.strip()

        # Ignorer les lignes vides ou les en-têtes
        if not line or "Catégorie" in line or "RESULTATS" in line:
            continue

        # Déterminer la catégorie (TAXIS ou VTC)
        if line.startswith("TAXIS"):
            current_category = "TAXIS"
            line = line[5:].strip()  # Enlever "TAXIS"
        elif line.startswith("VTC"):
            current_category = "VTC"
            line = line[3:].strip()  # Enlever "VTC"

        # Parser la ligne candidat
        if current_category and line:
            candidate = _parse_candidate_line(line, current_category)
            if candidate:
                candidates.append(candidate)

    return candidates


def _parse_candidate_line(
    line: str, category: str
) -> Optional[Dict[str, Any]]:
    """
    Parse une ligne de candidat.

    Format : N° candidat Prénom NOM DECISION

    Args:
        line: Ligne candidat à parser.
        category: Catégorie (TAXIS ou VTC).

    Returns:
        Dictionnaire candidat ou None si parsing échoue.
    """
    # Regex pour extraire les parties
    # Pattern : numéro (lettres/chiffres) Prénom(s) NOM DECISION
    pattern = r"^([A-Z0-9]+)\s+([A-Za-zéèêëâôûœæç\s]+)\s+(ADMISSIBLE|NON-ADMISSIBLE)$"

    match = re.match(pattern, line, re.IGNORECASE)

    if match:
        numero, name_part, decision = match.groups()
        numero = numero.strip()
        decision = decision.upper()

        # Parser Prénom et NOM
        name_part = name_part.strip()
        parts = name_part.split()

        if len(parts) >= 2:
            prenom = parts[0]
            nom = " ".join(parts[1:])
        elif len(parts) == 1:
            prenom = parts[0]
            nom = ""
        else:
            return None

        return {
            "categorie": category,
            "numero_candidat": numero,
            "prenom": prenom,
            "nom": nom,
            "decision": decision,
        }

    return None


def _filter_admissibles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtre le DataFrame pour ne conserver que les candidats admissibles.

    Args:
        df: DataFrame source.

    Returns:
        DataFrame filtré.
    """
    df_filtered = df[
        df["decision"].astype(str).str.upper() == "ADMISSIBLE"
    ].copy()

    return df_filtered


__all__ = ["extract_admissibles_from_pdf"]
