from flask import Flask, request, redirect, url_for, flash, session, render_template
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Configuration de la clé secrète pour sécuriser les sessions
app.secret_key = os.getenv('SECRET_KEY')  # Utiliser la clé secrète depuis le fichier .env

# Récupération des identifiants PayPal à partir des variables d'environnement
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_SECRET = os.getenv('PAYPAL_SECRET')

# Vérifier si les variables d'environnement ont été correctement chargées
if not app.secret_key:
    raise ValueError("La clé secrète n'est pas configurée correctement dans le fichier .env.")
if not PAYPAL_CLIENT_ID or not PAYPAL_SECRET:
    raise ValueError("Les identifiants PayPal ne sont pas correctement configurés dans le fichier .env.")

@app.route('/return')
def return_url():
    """Route de retour après un paiement PayPal"""
    payer_id = request.args.get('PayerID')
    payment_id = request.args.get('paymentId')

    if payer_id and payment_id:
        try:
            # Logique simulée pour finaliser le paiement
            # Dans une implémentation réelle, vous devriez appeler l'API PayPal pour exécuter le paiement
            flash("Paiement approuvé avec succès !", 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Une erreur s'est produite lors du traitement du paiement : {str(e)}", 'danger')
            return redirect(url_for('dashboard'))
    else:
        flash("Échec du paiement. Les informations nécessaires ne sont pas complètes.", 'warning')
        return redirect(url_for('dashboard'))

@app.route('/process_payment')
def process_payment():
    """Route pour démarrer un processus de paiement (ajouter votre logique ici)"""
    return render_template('process_payment.html')

if __name__ == '__main__':
    # Démarrage de l'application Flask
    app.run(debug=True, port=5071)

@app.route('/routes')
def show_routes():
    """Affiche toutes les routes définies dans l'application Flask"""
    return "<br>".join([str(rule) for rule in app.url_map.iter_rules()])
