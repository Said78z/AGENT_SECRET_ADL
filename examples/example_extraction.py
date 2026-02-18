"""Exemple d'utilisation de extract_admissibles_from_pdf."""

from pathlib import Path
from agent_secret_adl.extraction import extract_admissibles_from_pdf

# Exemple 1 : Extraction simple depuis un PDF
if __name__ == "__main__":
    pdf_file = "data/admissibles_taxis_paris_201.pdf"
    output_file = "output/admissibles_paris_2024.csv"

    try:
        extract_admissibles_from_pdf(
            pdf_path=pdf_file,
            output_csv_path=output_file,
            departement="75",
            session_date="2024-01-15",
        )
        print(f"✅ Extraction réussie vers {output_file}")

    except FileNotFoundError:
        print(f"❌ Le fichier PDF {pdf_file} n'a pas été trouvé")
    except ValueError as e:
        print(f"❌ Erreur de traitement : {e}")
