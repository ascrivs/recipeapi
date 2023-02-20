from app.auth import blp as auth_blp
from flask.views import MethodView
from flask_smorest import abort
from flask_jwt_extended import jwt_required, get_jwt, create_access_token
from schemas import UserSchema
from app.models import User
from app import db
from datetime import datetime

@auth_blp.route('/users')
class AccountAdminView(MethodView):

    @jwt_required()
    @auth_blp.response(200, UserSchema(many=True))
    def get():
        jwt = get_jwt()
        if jwt.get("role") != 'administrator':
            abort(403, message="Administrator  privileges required.")
        else:
            users = User.query.all()
        return users
    
    @jwt_required()
    @auth_blp.arguments(UserSchema)
    @auth_blp.response(UserSchema)
    def post(user_data):
        jwt = get_jwt()
        if jwt.get("role") != 'administrator':
            abort(403, message="Administrator privileges required.")
        else:
            user = User(username=user_data["username"], password=user_data["password"], email=user_data["email"])
            db.session.add(user)
            db.session.commit()
            return user
    
@auth_blp.route('/login')
class AuthenticationView(MethodView):
    
    @auth_blp.arguments(UserSchema)
    def post(user_data):
        user = User.query.filter_by(email=user_data["email"]).first()

        if user.verify_password(user_data["password"]):
            add_claims = {
                "role": user.role,
                "iat": datetime.utcnow()
            }
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200
        user.failed_pwd += 1
        db.session.commit()
        abort (401, message="Invalid credentials.")