import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer les valeurs des variables d'environnement
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_SECRET = os.getenv('PAYPAL_SECRET')

# Vérifiez si les variables ont été chargées correctement
print("Client ID:", PAYPAL_CLIENT_ID)
print("Secret:", PAYPAL_SECRET)

