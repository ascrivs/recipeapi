from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()


def app_factory(configurations):
    app = Flask(__name__)

    app.config.from_object(config[configurations])
    
    db.init_app(app)


    Migrate(app=app, db=db)
#   Blueprint imports
    from app.recipes import blp as recipe_blp
    app.register_blueprint(recipe_blp)
    from app.ingredients import blp as ingredient_blp
    app.register_blueprint(ingredient_blp)


    
    return app