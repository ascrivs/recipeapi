from app.directions import blp as direct_blp
from flask.views import MethodView
from app.schemas import BaseDirectionSchema, UpdateDirectionSchema
from app.models import Direction
from app import db



@direct_blp.route('/direction/<int:direct_id>')
class DirectionView(MethodView):

    @direct_blp.response(200, BaseDirectionSchema)
    def get(direct_id):
        direction = Direction.query.filter_by(id=direct_id).first()
        return direction
    
    @direct_blp.response(201, UpdateDirectionSchema)
    def delete(direct_id):
        direct = Direction.query.filter_by(id=direct_id).first()
        db.session.delete(direct)
        db.session.commit()
        return direct




@direct_blp.route('/')
class AllDirectionsView(MethodView):

    @direct_blp.response(200, BaseDirectionSchema(many=True))
    def get():
        directions = Direction.query.all()
        return directions
    
    @direct_blp.arguments(BaseDirectionSchema)
    @direct_blp.response(201, BaseDirectionSchema)
    def post(direction_data):
        direction = Direction(direction_data['details'], recipe_id=direction_data['recipe_id'])
        db.session.add(direction)
        db.session.commit()
        return direction
