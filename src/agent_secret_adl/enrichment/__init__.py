"""Module d'enrichissement optionnel et low-scope des données candidates."""

from typing import List, Dict, Any, Optional

from .hunter import enrich_with_hunter
from .phones import enrich_with_phones


def enrich_candidates(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Enrichit les données candidates avec des informations supplémentaires.

    Enrichissement optionnel via APIs gratuites et sûres (ex. emails).

    Args:
        candidates: Liste de candidats à enrichir.

    Returns:
        Liste de candidats enrichis.

    Example:
        >>> candidates = [{"nom": "Jean Dupont"}]
        >>> enriched = enrich_candidates(candidates)
    """
    pass


def lookup_email(name: str, company: Optional[str] = None) -> Optional[str]:
    """
    Cherche un email pour une personne (via API gratuite si disponible).

    Args:
        name: Nom complet de la personne.
        company: Entreprise (optionnel).

    Returns:
        Email trouvé ou None.
    """
    pass


def is_enrichment_enabled() -> bool:
    """
    Vérifie si l'enrichissement est activé.

    Returns:
        True si l'enrichissement est activé.
    """
    pass


__all__ = [
    "enrich_candidates",
    "lookup_email",
    "is_enrichment_enabled",
    "enrich_with_hunter",
]
