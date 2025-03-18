import pandas as pd
import os

DATA_FILES = {
    "Appartements à louer": "appartements_a_louer_pretraites.csv",
    "Appartements meublés": "appartements_meubles_pretraites.csv",
    "Terrains à vendre": "terrains_a_vendre_pretraites1.csv",
    "Appartements à louer non prétraité":"appartement_a_louer.csv",
    "Appartements meublés non prétraité": "appartement_meuble.csv",
    "Terrains à vendre non prétraité": "terrain_a_vendre.csv"
}

def save_data(category, df):
    """Enregistre un DataFrame en CSV"""
    file_path = DATA_FILES[category]
    df.to_csv(file_path, index=False)

def load_data(category):
    """Charge un fichier CSV en DataFrame"""
    file_path = DATA_FILES.get(category, "")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None
