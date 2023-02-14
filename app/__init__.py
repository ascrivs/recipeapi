from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from flask_smorest import Api

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

#   Register SmoRest API and Blueprints

    api = Api(app)
    api.register_blueprint(recipe_blp)
    api.register_blueprint(ingredient_blp)
    



    
    return app