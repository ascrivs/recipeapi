from flask_smorest import Blueprint

blp = Blueprint('Auth', __name__, url_prefix='/auth',description='Operations for Authentication')

from app.auth.routes import routes