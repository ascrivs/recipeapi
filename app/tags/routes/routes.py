from app.tags import blp as tags_blp
from flask.views import MethodView
from flask_smorest import abort
from app import db
from app.models import Tag, recipe_tags
from app.schemas import BaseTagSchema, AllTagSchema


@tags_blp.route("/tag/<string:tag_id>")
class TagView(MethodView):

    @tags_blp.response(200, AllTagSchema)
    def get(self, tag_id):
        tag = Tag.query.filter_by(id=tag_id).first()
        return tag

    @tags_blp.arguments(BaseTagSchema)
    @tags_blp.response(201, BaseTagSchema)
    def put(self, tag_data, tag_id):
        tag = Tag.query.filter_by(id=tag_id).first()
        tag.name = tag_data['name']
        db.session.add(tag)
        db.session.commit()
        return tag

    @tags_blp.response(201, BaseTagSchema)
    def delete(self, tag_id):
        tag = Tag.query.filter_by(id=tag_id).first()
        if tag == None:
            abort(403, message="No tag found.")
        db.session.execute(recipe_tags.delete().where(recipe_tags.c.tag_id==tag_id))
        db.session.commit()
        return tag




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