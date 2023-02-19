from app.tags import blp as tags_blp
from flask.views import MethodView
from app import db
from app.models import Tag
from app.schemas import BaseTagSchema, AllTagSchema


@tags_blp.route("/tag/<int:tag_id>")
class TagView(MethodView):

    @tags_blp.response(200, AllTagSchema)
    def get(self, tag_id):
        tag = Tag.query.filter_by(id=tag_id).first()
        return tag

    def put(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass


@tags_blp.route("/")
class AllTagsView(MethodView):

    tags_blp.response(200, AllTagSchema(many=True))
    def get(self):
        tags = Tag.query.all()
        listed_tags = [tag.serialize() for tag in tags]
        return listed_tags

    @tags_blp.arguments(BaseTagSchema)
    @tags_blp.response(201, BaseTagSchema)
    def post(self, tag_data):
        new_tag = Tag(name=tag_data['name'])
        db.session.add(new_tag)
        db.session.commit()
        return new_tag