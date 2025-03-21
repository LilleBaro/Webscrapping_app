import pandas as pd
import os

# 📌 Dictionnaire des fichiers de données avec leurs noms de fichiers
DATA_FILES = {
    "Appartements à louer": "appartements_a_louer_pretraites.csv",
    "Appartements meublés": "appartements_meubles_pretraites.csv",
    "Terrains à vendre": "terrains_a_vendre_pretraites.csv",
    "Appartements à louer non prétraité": "appartement_a_louer.csv",
    "Appartements meublés non prétraité": "appartement_meuble.csv",
    "Terrains à vendre non prétraité": "terrain_a_vendre.csv"
}

# 📌 Répertoire où se trouvent les fichiers CSV
DATA_DIR = os.path.join('static')

def save_data(category, df):
    """
    Enregistre un DataFrame en CSV dans le dossier static/
    """
    if category not in DATA_FILES:
        raise ValueError(f"Catégorie inconnue : {category}")

    file_path = os.path.join(DATA_DIR, DATA_FILES[category])
    df.to_csv(file_path, index=False)
    print(f"✅ Données sauvegardées dans {file_path}")

def load_data1(category):
    """Charge un fichier CSV en DataFrame"""
    file_path = DATA_FILES.get(category, "")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

def load_data(category):
    """
    Charge un fichier CSV en DataFrame depuis le dossier static/
    """
    file_name = DATA_FILES.get(category)
    if not file_name:
        print(f"🚨 Catégorie inconnue : {category}")
        return None

    file_path = os.path.join(DATA_DIR, file_name)

    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            print(f"✅ Chargement réussi : {file_path}")
            return df
        except Exception as e:
            print(f"🚨 Erreur lors de la lecture du fichier {file_path} : {e}")
            return None
    else:
        print(f"🚨 Fichier introuvable : {file_path}")
        return None
