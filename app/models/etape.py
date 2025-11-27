from app.extensions import db

class Etape(db.Model):
    __tablename__ = 'etapes'
    id = db.Column(db.Integer, primary_key=True)
    ordre = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Clé étrangère vers la recette parente
    recette_id = db.Column(db.Integer, db.ForeignKey('recettes.id'), nullable=False)

    def to_dict(self):
        return {
            'ordre': self.ordre,
            'description': self.description
        }