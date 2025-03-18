from flask import Blueprint, render_template, request
import plotly.express as px
import pandas as pd
from utils.data_handler import load_data

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def show_dashboard():
    dataset_choice = request.args.get("dataset", "Appartements à louer")
    df = load_data(dataset_choice)

    if df is None or df.empty:
        return render_template("dashboard.html", error="Fichier introuvable. Veuillez scraper les données d'abord.")

    # 📌 Filtrage des données
    min_price = int(df["prix"].min()) if "prix" in df.columns else 0
    max_price = int(df["prix"].max()) if "prix" in df.columns else 10000000

    price_min = int(request.args.get("price_min", min_price))
    price_max = int(request.args.get("price_max", max_price))

    if "prix" in df.columns:
        df = df[(df["prix"] >= price_min) & (df["prix"] <= price_max)]

    selected_location = request.args.get("location", "Tous")
    if "adresse" in df.columns and selected_location != "Tous":
        df = df[df["adresse"] == selected_location]

    selected_rooms = request.args.getlist("rooms")
    if "nombre_chambre" in df.columns and selected_rooms:
        df = df[df["nombre_chambre"].astype(str).isin(selected_rooms)]

    # 📊 Génération des graphiques
    price_histogram = None
    price_vs_surface = None

    if "prix" in df.columns:
        price_histogram = px.histogram(df, x="prix", title="Distribution des prix", nbins=30).to_html(full_html=False)

    if "superficie" in df.columns and "prix" in df.columns:
        price_vs_surface = px.scatter(df, x="superficie", y="prix", title="Relation entre prix et Superficie", trendline="ols").to_html(full_html=False)

    return render_template("dashboard.html", 
                           df=df, 
                           dataset_choice=dataset_choice,
                           price_histogram=price_histogram, 
                           price_vs_surface=price_vs_surface,
                           price_min=price_min,
                           price_max=price_max,
                           selected_location=selected_location,
                           selected_rooms=selected_rooms)
