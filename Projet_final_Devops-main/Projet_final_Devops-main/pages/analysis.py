from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import os

analysis_bp = Blueprint('analysis', __name__)

# 📌 Route qui affiche la page d'analyse
@analysis_bp.route('/analysis', methods=['GET'])
def show_analysis_page():
    return render_template("analysis.html")

# 📌 Route qui charge le dataset depuis le dossier static
@analysis_bp.route('/load_data', methods=['GET'])
def load_dataset():
    dataset_choice = request.args.get("dataset")
    
    if not dataset_choice:
        return jsonify({"error": "Aucun dataset spécifié."}), 400

    # 📌 Construction du chemin complet vers le CSV dans static/
    file_path = os.path.join('static', f"{dataset_choice}.csv")

    if not os.path.exists(file_path):
        return jsonify({"error": "Fichier introuvable. Veuillez scraper les données d'abord."}), 404

    try:
        df = pd.read_csv(file_path)
        if df.empty:
            return jsonify({"error": "Le fichier est vide."}), 404
        # ✅ Conversion en JSON
        return jsonify({"data": df.to_dict(orient="records")})
    except Exception as e:
        return jsonify({"error": f"Erreur de lecture du fichier : {str(e)}"}), 500
