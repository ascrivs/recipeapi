from app.ingredients import blp as ingredient_blp
from flask_smorest import abort
from flask.views import MethodView


@ingredient_blp.route("/ingredients/ingredient/<string:ingredient_id>")
class IngredientView(MethodView):

    def get(self, ingredient_id):
        pass

    def put(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass


@ingredient_blp.route("/ingredients")
class AllIngredientView(MethodView):

    def get(self):
        pass