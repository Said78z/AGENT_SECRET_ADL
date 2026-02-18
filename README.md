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
```bash
python -m agent_secret_adl --help
```

## Architecture
Architecture simple et modulaire pour éviter la dette technique et faciliter l'évolution.
