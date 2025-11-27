from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.extensions import db


user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    
    users_list = [user.to_dict() for user in users]
    
    # 3. On renvoie la réponse JSON
    return jsonify(users_list), 200

@user_bp.route('/', methods=['POST'])
def create_user():
    # 1. On récupère les données envoyées par le client (le JSON)
    data = request.get_json()

    # 2. Petite validation : on vérifie que les champs sont bien là
    if not data or 'username' not in data or 'email' not in data or 'pwd'not in data :
        return jsonify({'error': 'Il manque le username ou l\'email'}), 400

    hashed_pwd = generate_password_hash(data['pwd'])
    new_user = User(
        username=data['username'],
        pwd=hashed_pwd,
        email=data['email']
    )

    try:
        # 4. On ajoute l'objet à la "session" (la zone d'attente)
        db.session.add(new_user)
        
        # 5. On valide la transaction (C'est là que le SQL INSERT part vers SQLite)
        db.session.commit()
        
        # 6. On renvoie l'utilisateur créé avec le code 201 (Created)
        return jsonify(new_user.to_dict()), 201

    except IntegrityError:
        # Si l'email ou le username existe déjà, SQLite renvoie une erreur
        db.session.rollback() # annulation de la requête en cas d'erreur
        return jsonify({'error': 'Cet utilisateur ou email existe déjà'}), 409