from flask import Flask
from config import DevelopmentConfig
from app.extensions import db, migrate

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. Initialiser les extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # 2. Enregistrer les Blueprints (les routes)
    from app.api.users import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')

    from app.api.recettes import recette_bp
    app.register_blueprint(recette_bp, url_prefix='/api/recettes')

    return app