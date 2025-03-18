from flask import Flask, render_template
from pages.scraping import scraping_bp
from pages.analysis import analysis_bp
from pages.dashboard import dashboard_bp
from pages.evaluation import evaluation_bp



app = Flask(__name__)

# Enregistrement des Blueprints
app.register_blueprint(scraping_bp, url_prefix='/scraping')
app.register_blueprint(analysis_bp, url_prefix='/analysis')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(evaluation_bp, url_prefix='/evaluation')


@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)


