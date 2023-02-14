from app.auth import blp as auth_blp
from flask.views import MethodView
from flask_smorest import abort
from flask_jwt_extended import jwt_required, get_jwt
from schemas import UserSchema
from app.models import User


class AuthView(MethodView):

    @jwt_required()
    @auth_blp.route('/users')
    @auth_blp.response(200, UserSchema(many=True))
    def get():
        jwt = get_jwt()
        if jwt.get("role") != 'administrator':
            abort(403, message="Administrator  privileges required.")
        else:
            users = User.query.all()
        return users