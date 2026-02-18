"""Agent Secret ADL - Extraction et enrichissement de candidatures TAXIS/VTC."""

__version__ = "0.1.0"
__author__ = "AGENT_SECRET_ADL"

from . import config, extraction, normalization, enrichment, reporting

__all__ = ["config", "extraction", "normalization", "enrichment", "reporting"]
