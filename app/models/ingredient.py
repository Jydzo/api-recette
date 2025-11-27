from app.extensions import db

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    quantite = db.Column(db.String(50), nullable=False)

    # Clé étrangère vers la recette parente
    recette_id = db.Column(db.Integer, db.ForeignKey('recettes.id'), nullable=False)

    def to_dict(self):
        return {
            'nom': self.nom,
            'quantite': self.quantite
        }