from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'clé_par_défaut_si_non_trouvée')

# Configuration de la base de données
# Assurez-vous que le chemin est relatif à votre sous-dossier 'jeux-de-dames'
instance_folder = os.path.join(os.path.dirname(__file__), 'instance')
db_path = os.path.join(instance_folder, 'user.db')

# Créer le dossier 'instance' dans le sous-dossier 'jeux-de-dames' s'il n'existe pas
if not os.path.exists(instance_folder):
    os.makedirs(instance_folder)

# Supprimer la création automatique du fichier 'user.db'
if not os.path.exists(db_path):
    print("Le fichier 'user.db' n'existe pas. Vous devrez peut-être le créer manuellement ou via l'application.")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=0.0)

# Page d'accueil
@app.route('/')
def home():
    return render_template('home.html')

# Page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if not username or not password:
            flash("Veuillez remplir tous les champs.", 'warning')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Connexion réussie !', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.", 'danger')
    return render_template('login.html')

# Page de récupération de mot de passe
@app.route('/recover_password', methods=['GET', 'POST'])
def recover_password():
    if request.method == 'POST':
        email = request.form['email'].strip()
        if not email:
            flash("Veuillez entrer un e-mail valide.", 'warning')
            return redirect(url_for('recover_password'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Instructions de récupération envoyées à votre adresse e-mail.', 'info')
        else:
            flash("Aucun utilisateur n'a été trouvé avec cet e-mail.", 'warning')
        return redirect(url_for('login'))
    return render_template('recover_password.html')

# Page d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        email = request.form['email'].strip()
        last_name = request.form['last_name'].strip()
        first_name = request.form['first_name'].strip()
        date_of_birth = request.form['date_of_birth'].strip()
        postal_code = request.form['postal_code'].strip()

        # Validation des champs obligatoires
        if not all([username, password, email, last_name, first_name, date_of_birth, postal_code]):
            flash("Tous les champs doivent être remplis.", 'warning')
            return redirect(url_for('register'))

        # Validation de la longueur du mot de passe
        if len(password) < 6:
            flash("Le mot de passe doit comporter au moins 6 caractères.", 'danger')
            return redirect(url_for('register'))

        # Validation de la date de naissance
        try:
            datetime.strptime(date_of_birth, '%Y-%m-%d')
        except ValueError:
            flash("La date de naissance est invalide.", 'danger')
            return redirect(url_for('register'))

        # Vérification si l'utilisateur ou l'email existe déjà
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash("Cet utilisateur ou cet e-mail existe déjà.", 'warning')
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            password=generate_password_hash(password),
            email=email,
            last_name=last_name,
            first_name=first_name,
            date_of_birth=datetime.strptime(date_of_birth, '%Y-%m-%d').date(),
            postal_code=postal_code
        )
        
        db.session.add(new_user)
        db.session.commit()

        # Connexion automatique de l'utilisateur après l'inscription
        session['user_id'] = new_user.id
        flash('Inscription réussie ! Vous êtes maintenant connecté.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

# Tableau de bord
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Vous devez être connecté pour accéder au tableau de bord.", 'info')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    users_online = User.query.count()  # Compter tous les utilisateurs
    return render_template('dashboard.html', user=user, users_online=users_online)

# Déconnexion
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Vous vous êtes déconnecté avec succès.", 'info')
    return redirect(url_for('login'))

# Initialisation de la base de données
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Base de données initialisée avec succès !")

    app.run(debug=True, port=5023)
