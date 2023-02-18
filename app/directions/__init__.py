from flask_smorest import Blueprint

blp = Blueprint("Directions", __name__, description="Operations on Directions",url_prefix="/directions")

from app.directions.routes import routes