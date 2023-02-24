from app.auth import blp as auth_blp
from flask import jsonify
from flask.views import MethodView
from flask_smorest import abort
from flask_jwt_extended import jwt_required, get_jwt, create_access_token, get_jwt_identity, create_refresh_token
from app.schemas import UserSchema
from app.models import User
from app import db, jwt
from datetime import datetime


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

@auth_blp.route('/refresh')
class AccountAuthentication(MethodView):

    @jwt_required(refresh=True)
    def refresh(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token)


@auth_blp.route('/users')
class AccountAdminView(MethodView):

    @jwt_required(fresh=True)
    @auth_blp.response(200, UserSchema(many=True))
    def get(self):
        jwt = get_jwt()
        if jwt.get("role") != 'administrator':
            abort(403, message="Administrator  privileges required.")
        else:
            User.ping()
            users = User.query.all()
        return users
    
    @jwt_required(fresh=True)
    @auth_blp.arguments(UserSchema)
    @auth_blp.response(201, UserSchema)
    def post(self, user_data):
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
    def post(self, user_data):
        user = User.query.filter_by(email=user_data["email"]).first()

        if user.verify_password(user_data["password"]) and not user.account_locked:
            add_claims = {
                "role": user.role,
                "iat": datetime.utcnow(),
                "id": user.id
            }
            access_token = create_access_token(identity=user.id, additional_claims=add_claims)
            refresh_token = create_refresh_token(identity=user.id, additional_claims=add_claims)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        if user.account_locked:
            abort(401, message="Account is locked out.")
        abort (401, message="Invalid credentials.")