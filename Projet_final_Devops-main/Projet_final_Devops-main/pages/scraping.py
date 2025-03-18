from flask import Blueprint, render_template, request, jsonify
import os
import pandas as pd
from scraper import*

scraping_bp = Blueprint('scraping', __name__)

# 📌 Route principale pour afficher la page de scraping
@scraping_bp.route('/scraping', methods=['GET'])
def show_scraping_page():
    return render_template('scraping.html', categories=URLS.keys())

# 📌 Route pour exécuter le scraping et retourner les résultats en JSON
@scraping_bp.route('/scraping/scrape', methods=['POST'])
def run_scraping():
    data = request.get_json()
    category = data.get("category")
    max_pages = int(data.get("max_pages", 5))

    if category not in URLS:
        return jsonify({"success": False, "message": "Catégorie invalide."})

    # Exécuter le scraping
    annonces = scrape_expat_dakar(URLS[category], max_pages)

    if not annonces:
        return jsonify({"success": False, "message": "Aucune annonce trouvée."})

    # Sauvegarder en CSV
    csv_filename = f"static/{category.replace(' ', '_')}.csv"
    pd.DataFrame(annonces).to_csv(csv_filename, index=False)

    return jsonify({
        "success": True,
        "message": f"{len(annonces)} annonces récupérées.",
        "annonces": annonces,
        "csv_filename": csv_filename
    })
