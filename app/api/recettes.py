from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from app.models.recette import Recette
from app.models.etape import Etape
from app.models.ingredient import Ingredient
from app.extensions import db


recette_bp = Blueprint('recettes', __name__)

@recette_bp.route('/', methods=['GET'])
def get_recettes():
    recettes = Recette.query.all()
    
    recettes_list = [recette.to_dict() for recette in recettes]
    
    # 3. On renvoie la réponse JSON
    return jsonify(recettes_list), 200

@recette_bp.route('/', methods=['POST'])
def create_recette():
    # 1. On récupère les données envoyées par le client (le JSON)
    data = request.get_json()

    # 2. Petite validation : on vérifie que les champs sont bien là
    if not data or 'titre' not in data or 'temp' not in data or 'ingredients' not in data or 'etapes' not in data or 'user_id' not in data:
        return jsonify({'error': 'Il manque des données'}), 400

    try:
        print('<p>recette</p>')
        n_recette = Recette(
            titre=data['titre'],
            temp=data['temp'],
            user_id=data['user_id']
        )
        db.session.add(n_recette)
        db.session.flush()

        for ingredient in data['ingredients']:
            n_ingredient = Ingredient(
                nom =  ingredient['nom'],
                quantite =  ingredient['quantite'],
                recette_id = n_recette.id  
            )
            db.session.add(n_ingredient)

        for i, etape in enumerate(data['etapes']):
            n_etape = Etape(
                ordre = i + 1,
                description =  etape['description'],
                recette_id = n_recette.id   
            )
            db.session.add(n_etape)
        
        # 5. On valide la transaction (C'est là que le SQL INSERT part vers SQLite)
        db.session.commit()
        return jsonify(n_recette.to_dict()), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Erreur : Problème de doublon de titre.'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur de traitement des données: {str(e)}'}), 500