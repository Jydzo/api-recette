from app.extensions import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pwd = db.Column(db.String(126),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    recipes = db.relationship('Recette', backref='author', lazy=True, cascade='all, delete-orphan')
    
    # Bonne pratique : une méthode pour convertir l'objet en dictionnaire (JSON)
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
