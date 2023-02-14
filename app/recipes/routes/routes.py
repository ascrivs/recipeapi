from app.recipes import blp as recipe_blp
from flask_smorest import abort
from flask.views import MethodView


@recipe_blp.route("/recipes/<string:recipe_id>")
class RecipeView(MethodView):
    def get(self, recipe_id):
        return recipe_id
    
    def delete(self, recipe_id):
        pass

    def post(self, recipe):
        pass

    def post(self, recipe):
        pass


@recipe_blp.route("/recipes")
class AllRecipesView(MethodView):

    def get(self):
        pass


