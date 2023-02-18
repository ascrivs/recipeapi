from app.tags import blp as tags_blp
from flask.views import MethodView
from app import db
from app.models import Tag
from app.schemas import BaseTagSchema


@tags_blp.route("/tag/<int:tag_id>")
class TagView(MethodView):


    def get(self, tag_id):
        pass

    def put(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass



@tags_blp.route("/")
class AllTagsView(MethodView):

    tags_blp.response(200, BaseTagSchema(many=True))
    def get(self):
        return Tag.query.all()

    @tags_blp.arguments(BaseTagSchema)
    @tags_blp.arguments(201, BaseTagSchema)
    def post(self, tag_data):
        new_tag = Tag(name=tag_data['name'])
        db.session.add(new_tag)
        db.session.commit()
        return new_tag