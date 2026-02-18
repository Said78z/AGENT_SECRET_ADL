"""Module d'extraction de données depuis des documents PDF."""

from typing import List, Dict, Any

from .extract_admissibles import extract_admissibles_from_pdf


def extract_from_pdf(file_path: str) -> List[Dict[str, Any]]:
    """
    Extrait les listes de candidats depuis un fichier PDF.

    Args:
        file_path: Chemin vers le fichier PDF.

    Returns:
        Liste de dictionnaires contenant les données extraites.

    Example:
        >>> candidates = extract_from_pdf("document.pdf")
        >>> print(len(candidates))
    """
    pass


def validate_extraction(data: List[Dict[str, Any]]) -> bool:
    """
    Valide les données extraites.

    Args:
        data: Données d'extraction à valider.

    Returns:
        True si les données sont valides, False sinon.
    """
    pass


__all__ = [
    "extract_from_pdf",
    "validate_extraction",
    "extract_admissibles_from_pdf",
]
