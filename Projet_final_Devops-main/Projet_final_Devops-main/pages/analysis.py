from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import os

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analysis', methods=['GET'])
def show_analysis_page():
    return render_template("analysis.html")

@analysis_bp.route('/load_data', methods=['GET'])
def load_dataset():
    dataset_choice = request.args.get("dataset")
    
    if not dataset_choice:
        return jsonify({"error": "Aucun dataset spécifié."}), 400

    # ✅ Nettoyage du nom et construction du chemin dans le dossier static
    safe_filename = dataset_choice.replace(' ', '_') + ".csv"
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    file_path = os.path.join(static_dir, safe_filename)

    if not os.path.exists(file_path):
        return jsonify({"error": f"Fichier {safe_filename} introuvable dans static."}), 404

    try:
        df = pd.read_csv(file_path)
        if df.empty:
            return jsonify({"error": "Le fichier est vide."}), 404
        return jsonify({"data": df.to_dict(orient="records")})
    except Exception as e:
        return jsonify({"error": f"Erreur de lecture du fichier : {str(e)}"}), 500
