from app.extensions import db

class Recette(db.Model):
    __tablename__ = 'recettes'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80), unique=True, nullable=False)
    temp = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ingredients = db.relationship('Ingredient', backref='recette', lazy=True, cascade='all, delete-orphan')
    etapes = db.relationship('Etape', backref='recette', lazy=True, cascade='all, delete-orphan')
    
    # conversion en json
    def to_dict(self):
        return {
            'id': self.id,
            'tire': self.titre,
            'temp': self.temp,
            'user_id': self.user_id,
            'ingredients': [ingredient.to_dict() for ingredient in self.ingredients],
            'etapes': [etape.to_dict() for etape in self.etapes]
        }
