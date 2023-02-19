from app.directions import blp as direct_blp
from flask.views import MethodView
from app.schemas import BaseDirectionSchema, UpdateDirectionSchema
from app.models import Direction
from app import db



@direct_blp.route('/direction/<string:direct_id>')
class DirectionView(MethodView):

    @direct_blp.response(200, BaseDirectionSchema)
    def get(self, direct_id):
        direction = Direction.query.filter_by(id=direct_id).first()
        return direction
    
    @direct_blp.response(201, UpdateDirectionSchema)
    def delete(self, direct_id):
        direct = Direction.query.filter_by(id=direct_id).first()
        db.session.delete(direct)
        db.session.commit()
        return direct

    @direct_blp.response(201, UpdateDirectionSchema)
    def put(self, direct_data, direct_id):
        direction = Direction.query.filter_by(id=direct_id)
        direction.details = direct_data["details"]
        db.session.add(direction)
        db.session.commit()
        return direction




@direct_blp.route('/')
class AllDirectionsView(MethodView):

    @direct_blp.response(200, BaseDirectionSchema(many=True))
    def get(self):
        directions = Direction.query.all()
        return directions
    
    @direct_blp.arguments(BaseDirectionSchema)
    @direct_blp.response(201, BaseDirectionSchema)
    def post(self, direction_data):
        direction = Direction(details=direction_data['details'], recipe_id=direction_data['recipe_id'])
        db.session.add(direction)
        db.session.commit()
        return direction
