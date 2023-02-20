from app.directions import blp as direct_blp
from flask_smorest import abort
from flask.views import MethodView
from app.schemas import BaseDirectionSchema, UpdateDirectionSchema
from app.models import Direction, Recipe
from app import db
from flask_jwt_extended import jwt_required, get_jwt



@direct_blp.route('/direction/<string:direct_id>')
class DirectionView(MethodView):

    @direct_blp.response(200, BaseDirectionSchema)
    def get(self, direct_id):
        direction = Direction.query.filter_by(id=direct_id).first()
        return direction
    
    @jwt_required()
    @direct_blp.response(201, UpdateDirectionSchema)
    def delete(self, direct_id):
        jwt = get_jwt()
        direct = Direction.query.filter_by(id=direct_id).first()
        recipe = Recipe.query.filter_by(id=direct.recipe_id).first()
        if jwt.get('id') == recipe.created_by:
            db.session.delete(direct)
            db.session.commit()
            return direct
        abort(403, message="Access denied.")

    @jwt_required()
    @direct_blp.response(201, UpdateDirectionSchema)
    def put(self, direct_data, direct_id):
        jwt = get_jwt()
        direct = Direction.query.filter_by(id=direct_id).first()
        recipe = Recipe.query.filter_by(id=direct.recipe_id).first()
        if jwt.get('id') == recipe.created_by:
            direct.details = direct_data["details"]
            db.session.add(direct)
            db.session.commit()
            return direct




@direct_blp.route('/')
class AllDirectionsView(MethodView):

    @direct_blp.response(200, BaseDirectionSchema(many=True))
    def get(self):
        directions = Direction.query.all()
        return directions
    
    @jwt_required()
    @direct_blp.arguments(BaseDirectionSchema)
    @direct_blp.response(201, BaseDirectionSchema)
    def post(self, direction_data):
        jwt = get_jwt()
        if jwt.get('id') == Recipe.query.filter_by(id=direction_data['recipe_id']).first().created_by:
            direction = Direction(details=direction_data['details'], recipe_id=direction_data['recipe_id'])
            db.session.add(direction)
            db.session.commit()
            return direction
        abort(403, message="Access denied.")
