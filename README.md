# 🚕 AGENT_SECRET_ADL

Outil pour extraire les candidats **ADMISSIBLE** depuis des PDF officiels TAXIS/VTC en France, et récupérer leurs **téléphones + emails**.

---

## ⚙️ Installation (Une seule fois)

```bash
cd /home/saidk/agent_vtc/AGENT_SECRET_ADL

# Crée un environnement Python
python3 -m venv venv
source venv/bin/activate

# Installe les dépendances
pip install -r requirements.txt
```

---

## 🎯 Utilisation

### Étape 1 : Mets ton PDF ici
```bash
# Place ton fichier PDF dans le dossier
# Exemple: 2025_FEV_ADMISSIBLES_MARSEILLE.pdf
```

### Étape 2 : Lance la commande
```bash
# Remplace les valeurs avec tes infos
python -m agent_secret_adl.cli extract-admissibles \
    --pdf-path 2025_FEV_ADMISSIBLES_MARSEILLE.pdf \
    --output-csv resultats.csv \
    --departement 13 \
    --session-date 2025-02-18
```

**Résultat** : `resultats.csv` avec tous les candidats ADMISSIBLE ✅

### (Optionnel) Étape 3 : Ajoute les téléphones + emails
```bash
python -m agent_secret_adl.cli enrich-phones \
    --input-csv resultats.csv \
    --output-csv resultats_complets.csv
```

**Résultat** : `resultats_complets.csv` avec téléphones + emails ✅

---

## 📋 Colonnes du CSV final

```
categorie,numero_candidat,prenom,nom,decision,departement,session_date,email,phone,phone_source
TAXIS,527805,Zineb,AIT ELDJOUDI,ADMISSIBLE,78,2025-02-25,zineb.aiteldjoudi@example.com,01 23 45 67 89,SIRENE
VTC,494980,Faysale,AIT BIHI,ADMISSIBLE,78,2025-02-25,faysale.aitbihi@example.com,02 12 34 56 78,Pages Jaunes
```

---

## 🔧 Paramètres

### extract-admissibles
- `--pdf-path` : Chemin du fichier PDF (requis)
- `--output-csv` : Chemin du CSV de sortie (requis)
- `--departement` : Code département (ex: 78, 13, Paris)
- `--session-date` : Date session (ex: 2025-02-25)

### enrich-phones
- `--input-csv` : CSV d'entrée (requis)
- `--output-csv` : CSV de sortie (requis)
- `--max-rows` : Nombre max de candidats à traiter (défaut: 50)

---

## 📊 Exemple Complet

```bash
# 1. Extraction
python -m agent_secret_adl.cli extract-admissibles \
    --pdf-path admissibles.pdf \
    --output-csv step1.csv \
    --departement 78 \
    --session-date 2025-02-25

# 2. Enrichissement (mails + tels)
python -m agent_secret_adl.cli enrich-phones \
    --input-csv step1.csv \
    --output-csv step2_final.csv

# 3. Vérifie le résultat
head step2_final.csv
```

---

## ✅ Ce qui fonctionne

✓ Extraction PDF (parsing intelligent)  
✓ Filtrage ADMISSIBLE uniquement  
✓ Téléphones (SIRENE, Pages Jaunes, etc.)  
✓ Emails (Hunter.io)  
✓ CSV propre et structuré  
✓ Format FR standard pour numéros  

---

## 🆘 Debug

```bash
# Mode verbose (logs détaillés)
python -m agent_secret_adl.cli extract-admissibles \
    --pdf-path file.pdf \
    --output-csv out.csv \
    --departement 78 \
    --session-date 2025-02-25 \
    --verbose
```

---

**C'est tout ce que tu dois savoir ! 🚀**
