from flask_smorest import Blueprint

blp = Blueprint("Ingredients", __name__, description="Operations on Directions",url_prefix="/directions")

from app.directions.routes import routes