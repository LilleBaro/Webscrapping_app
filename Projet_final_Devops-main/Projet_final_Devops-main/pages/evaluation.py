from flask import Blueprint, render_template, request, flash, redirect, url_for
import smtplib
from email.message import EmailMessage

evaluation_bp = Blueprint('evaluation', __name__)

# 📌 Configuration de l'e-mail
EMAIL_SENDER = "iss654864@gmail.com"
EMAIL_PASSWORD = "fjxhsladuowjkygl"
EMAIL_RECEIVER = "ibrahimasorysane986@gmail.com"

def send_email(user_email, rating, comment):
    """ Envoie un e-mail avec l'évaluation """
    try:
        msg = EmailMessage()
        msg.set_content(f"""
        📌 Nouvelle évaluation de l'application
        
        ⭐ Note donnée : {rating} étoiles
        💬 Commentaire : {comment}
        ✉️ Adresse e-mail de l'utilisateur : {user_email}
        """)

        msg["Subject"] = "Nouvelle Évaluation de l'application"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")
        return False

# 📌 Route pour afficher la page d'évaluation et gérer l'envoi du formulaire
@evaluation_bp.route('/evaluation', methods=['GET', 'POST'])
def show_evaluation_page():
    if request.method == 'POST':
        user_email = request.form['user_email']
        rating = request.form['rating']
        comment = request.form['comment']

        if user_email and comment:
            success = send_email(user_email, rating, comment)
            if success:
                flash("Merci pour votre évaluation ! Votre message a été envoyé.", "success")
            else:
                flash("Une erreur est survenue lors de l'envoi du message. Réessayez plus tard.", "danger")
        else:
            flash("Veuillez remplir tous les champs.", "warning")

        return redirect(url_for('evaluation.show_evaluation_page'))

    return render_template('evaluation.html')
