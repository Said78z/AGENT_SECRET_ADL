# Module Extraction - Documentation Technique

## Vue d'ensemble

Le module `extraction` extrait les listes de candidats admissibles depuis des documents PDF officiels.

## Fonction Principale : `extract_admissibles_from_pdf`

### Signature

```python
def extract_admissibles_from_pdf(
    pdf_path: str,
    output_csv_path: str,
    departement: str,
    session_date: str,
) -> None:
```

### Paramètres

| Paramètre | Type | Description |
|-----------|------|-------------|
| `pdf_path` | `str` | Chemin vers le fichier PDF à traiter |
| `output_csv_path` | `str` | Chemin de destination pour le fichier CSV |
| `departement` | `str` | Code ou nom du département (ex: "75", "Paris") |
| `session_date` | `str` | Date de la session (ex: "2024-01-15") |

### Comportement

1. **Validation** : Vérifie que le fichier PDF existe et est valide
2. **Extraction** : Parcourt chaque page du PDF et extrait les tableaux
3. **Normalisation** : Convertit les tableaux en dictionnaires avec en-têtes normalisés
4. **Filtrage** : Conserve uniquement les lignes où `decision == "ADMISSIBLE"`
5. **Métadonnées** : Ajoute les colonnes `departement` et `session_date`
6. **Export** : Sauvegarde le résultat en CSV (UTF-8, index=False)

### Gestion des Erreurs

- **`FileNotFoundError`** : Le fichier PDF n'existe pas
- **`ValueError`** : Format invalide ou pas de donnée pertinente
- **`RuntimeError`** : Erreur inattendue lors du traitement

### Logging

La fonction utilise le logging standard Python (`logging` module) avec les niveaux :
- `INFO` : Début extraction, nombre de pages, candidats trouvés
- `WARNING` : Pas de colonne decision, pas d'admissibles
- `DEBUG` : Détails par page
- `ERROR` : Erreurs critiques

## Fonctions Auxiliaires

### `_extract_tables_from_pdf(pdf_path)`
- Extrait tous les tableaux de toutes les pages
- Gère les erreurs de parsing par page
- Retourne une liste de dictionnaires

### `_normalize_table(table)`
- Convertit un tableau PDF en liste de dictionnaires
- Les en-têtes sont normalisés (minuscules, underscores)
- Gère les cellules vides

### `_filter_admissibles(df)`
- Filtre le DataFrame sur la colonne "decision"
- Cherche la colonne contenant "decision" (insensible à la casse)
- Compare "ADMISSIBLE" (insensible à la casse)

## Exemple d'Utilisation

### Via CLI

```bash
python -m agent_secret_adl extract \
  data/admissibles_paris.pdf \
  --output results/paris_admissibles.csv \
  --departement 75 \
  --session-date 2024-01-15
```

### Via Python

```python
from agent_secret_adl.extraction import extract_admissibles_from_pdf

try:
    extract_admissibles_from_pdf(
        pdf_path="data/admissibles_paris.pdf",
        output_csv_path="results/paris_admissibles.csv",
        departement="75",
        session_date="2024-01-15",
    )
    print("✅ Extraction réussie")
except FileNotFoundError as e:
    print(f"❌ Erreur : {e}")
except ValueError as e:
    print(f"❌ Erreur de traitement : {e}")
```

## CSV de Sortie

Les colonnes du CSV exporté contiennent :
- Colonnes du tableau PDF original (avec en-têtes normalisés)
- `departement` : Code/nom du département fourni
- `session_date` : Date de la session fournie

Exemple de structures possibles :
```
categorie,numero_candidat,prenom,nom,decision,departement,session_date
TAXI,001,Jean,Dupont,ADMISSIBLE,75,2024-01-15
VTC,002,Marie,Martin,ADMISSIBLE,75,2024-01-15
```

## Dépendances

- `pdfplumber` : Extraction de tableaux PDF
- `pandas` : Manipulation de DataFrames
- `logging` : Logging standard Python

## Architecture

Le module suit une architecture simple :
- **Fonction publique** : `extract_admissibles_from_pdf`
- **Fonctions privées** : Logique métier décomposée (`_extract_tables_from_pdf`, `_normalize_table`, `_filter_admissibles`)
- **Logging** : Visibilité sur les étapes et erreurs
- **Gestion d'erreurs** : Exceptions explicites et messages clairs
