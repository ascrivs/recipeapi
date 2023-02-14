from flask_smorest import Blueprint


blp = Blueprint('Recipes',__name__, description="Operations on Recipes",url_prefix="/recipes")

from app.recipes.routes import routes