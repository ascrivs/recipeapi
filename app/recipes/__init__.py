from flask_smorest import Blueprint


blp = Blueprint('recipes',__name__, description="Operations on Recipes",url_prefix="/recipes")