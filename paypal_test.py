import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Identifiants PayPal (récupérés depuis le fichier .env)
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_SECRET = os.getenv('PAYPAL_SECRET')

# Fonction pour obtenir un jeton d'accès PayPal
def get_access_token():
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET), data=data)
    
    if response.status_code == 200:
        print("Token d'accès récupéré avec succès.")
        return response.json()['access_token']
    else:
        print("Erreur lors de la récupération du token d'accès :", response.status_code, response.text)
        return None

# Fonction pour créer un paiement
def create_payment():
    access_token = get_access_token()
    if not access_token:
        return

    url = "https://api.sandbox.paypal.com/v1/payments/payment"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payment_data = {
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": "10.00",  # Montant du paiement
                "currency": "USD"  # Devise
            },
            "description": "Transaction de test avec PayPal"
        }],
        "redirect_urls": {
            "return_url": "http://localhost:8000/return",  # URL de retour en cas de succès
            "cancel_url": "http://localhost:8000/cancel"  # URL en cas d'annulation
        }
    }

    response = requests.post(url, json=payment_data, headers=headers)

    if response.status_code == 201:  # 201 = Created
        print("Paiement créé avec succès.")
        payment = response.json()
        print("ID de paiement :", payment['id'])
        
        # Lien d'approbation pour rediriger l'utilisateur
        for link in payment['links']:
            if link['rel'] == 'approval_url':
                print("Lien pour approuver le paiement :", link['href'])
    else:
        print("Erreur lors de la création du paiement :", response.status_code, response.text)

# Appel de la fonction pour créer un paiement
create_payment()
