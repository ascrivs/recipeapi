from flask_smorest import Blueprint


blp = Blueprint('Ingredients', __name__, description="Operations on Ingredients",url_prefix="/ingredients")