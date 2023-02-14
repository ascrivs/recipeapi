from app.tags import blp as tags_blp
from flask.views import MethodView


@tags_blp.route("/tags/tag/<string:tag_id>")
class TagView(MethodView):


    def get(self, tag_id):
        pass

    def put(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass



@tags_blp.route("/tags")
class AllTagView(MethodView):

    def get(self):
        pass