from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Créez une instance de SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    nom = db.Column(db.String(150), nullable=False)
    prenom = db.Column(db.String(150), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)  # Augmenté à 200 caractères
    code_postal = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Pour accueillir des mots de passe hachés plus longs
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)  # Ajout de la date de création

    def __repr__(self):
        return f'<User {self.username}>'
