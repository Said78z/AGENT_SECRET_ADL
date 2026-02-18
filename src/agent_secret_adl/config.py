"""Configuration globale du projet AGENT_SECRET_ADL."""

from pathlib import Path

# Chemins principaux
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
LOGS_DIR = PROJECT_ROOT / "logs"

# Créer les répertoires s'ils n'existent pas
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Configuration d'extraction
EXTRACTION_CONFIG = {
    "supported_formats": ["pdf"],
    "encoding": "utf-8",
}

# Configuration de normalisation
NORMALIZATION_CONFIG = {
    "normalize_spaces": True,
    "lowercase_fields": ["email", "phone"],
}

# Configuration d'enrichissement
ENRICHMENT_CONFIG = {
    "enabled": False,
    "timeout": 5,
    "retry_count": 2,
}

# Configuration de reporting
REPORTING_CONFIG = {
    "output_format": "csv",
    "delimiter": ",",
    "include_metadata": True,
}

# Logging
LOGGING_LEVEL = "INFO"
