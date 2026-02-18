# AGENT_SECRET_ADL

**Agent Secret ADL** est un outil léger et modulaire pour extraire, normaliser et enrichir les listes de candidats admissibles aux licences TAXIS et VTC depuis des documents PDF officiels.

## Fonctionnalités
- **Extraction** : Récupère les données candidates depuis des PDF
- **Normalisation** : Nettoie et standardise les informations
- **Enrichissement** (optionnel) : Ajoute des données supplémentaires via APIs gratuites
- **Reporting** : Exporte les résultats en CSV structuré

## Installation
```bash
pip install -r requirements.txt
```

## Structure du projet
```
src/
  agent_secret_adl/
    config.py           # Configuration globale
    extraction/         # Module d'extraction PDF
    normalization/      # Module de normalisation
    enrichment/         # Module d'enrichissement optionnel
    reporting/          # Module de reporting CSV
```

## Usage

### Via CLI
```bash
# Afficher l'aide
python -m agent_secret_adl --help

# Extraire les admissibles depuis un PDF
python -m agent_secret_adl extract \
  data/admissibles.pdf \
  --output output/admissibles.csv \
  --departement 75 \
  --session-date 2024-01-15
```

### Via Python
```python
from agent_secret_adl.extraction import extract_admissibles_from_pdf

extract_admissibles_from_pdf(
    pdf_path="data/admissibles.pdf",
    output_csv_path="output/admissibles.csv",
    departement="75",
    session_date="2024-01-15",
)
```

## Architecture
Architecture simple et modulaire pour éviter la dette technique et faciliter l'évolution.

## Modules

- **extraction** : Extraction des listes depuis PDF
- **normalization** : Nettoyage et standardisation des données
- **enrichment** : Enrichissement optionnel (emails, etc.)
- **reporting** : Export en CSV et génération de rapports
