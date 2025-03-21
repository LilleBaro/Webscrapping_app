from flask import Blueprint, render_template, request, jsonify
import pandas as pd
from scraper import scrape_expat_dakar
import os

scraping_bp = Blueprint('scraping', __name__)

URLS = {
    "Appartements à louer": "https://www.expat-dakar.com/appartements-a-louer",
    "Appartements meublés": "https://www.expat-dakar.com/appartements-meubles",
    "Terrains à vendre": "https://www.expat-dakar.com/terrains-a-vendre"
}

# ✅ Route pour afficher la page scraping
@scraping_bp.route('/scraping', methods=['GET'])
def show_scraping_page():
    return render_template('scraping.html', categories=URLS.keys())

# ✅ Route qui lance le scraping et renvoie les résultats
@scraping_bp.route('/scrape', methods=['POST'])
def run_scraping():
    data = request.get_json()
    category = data.get("category")
    max_pages = int(data.get("max_pages", 5))

    if category not in URLS:
        return jsonify({"success": False, "message": "Catégorie invalide."})

    try:
        # 📌 Lancement du scraping
        df = scrape_expat_dakar(URLS[category], max_pages)

        if df.empty:
            return jsonify({"success": False, "message": "Aucune annonce trouvée."})

        # 📌 Sauvegarde dans le dossier static
        csv_filename = f"static/{category.replace(' ', '_')}.csv"
        df.to_csv(csv_filename, index=False)

        # 📌 Réponse JSON avec les résultats et le lien de téléchargement
        return jsonify({
            "success": True,
            "message": f"{len(df)} annonces récupérées.",
            "annonces": df.to_dict(orient="records"),
            "csv_filename": csv_filename
        })

    except Exception as e:
        return jsonify({"success": False, "message": f"Erreur lors du scraping : {str(e)}"})
