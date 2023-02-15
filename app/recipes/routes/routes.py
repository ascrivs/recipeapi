from app.recipes import blp as recipe_blp
from flask_smorest import abort
from flask.views import MethodView
from app.schemas import BaseRecipeSchema
from app.models import Recipe, Direction, Ingredient, Tag
from app import db


@recipe_blp.route("/recipe/<string:recipe_id>")
class RecipeView(MethodView):
    def get(self, recipe_id):
        return recipe_id
    
    def delete(self, recipe_id):
        pass
  
    def put(self, recipe):
        pass


@recipe_blp.route("/")
class AllRecipesView(MethodView):

    @recipe_blp.response(200, BaseRecipeSchema(many=True))
    def get(self):
        recipes = Recipe.query.all()
        return recipes


    @recipe_blp.arguments(BaseRecipeSchema)
    @recipe_blp.response(201, BaseRecipeSchema)
    def post(self, recipe):
        new_recipe = Recipe(name=recipe['name'].lower(),description=recipe['description'])
        db.session.add(new_recipe)
        db.session.commit()
        recipe_new_tags = []
        for recipe_tag in recipe['tags']:
            query_tag = recipe_tag['name'].lower()
            existing_tag = Tag.query.filter_by(name=query_tag).first()
            if existing_tag != None:
                recipe_new_tags.append(existing_tag)
            else:
                new_tag = Tag(name=query_tag)
                db.session.add(new_tag)
                recipe_new_tags.append(new_tag)
        for recipe_ingredient in recipe['ingredients']:
            new_ingredient = Ingredient(details=recipe_ingredient['details'], recipe_id=new_recipe.id)
            db.session.add(new_ingredient)
        for recipe_direction in recipe['directions']:
            new_direction = Direction(details=recipe_direction['details'], recipe_id=new_recipe.id)
            db.session.add(new_direction)
        db.session.commit()
        new_recipe.tags = recipe_new_tags
        db.session.add(new_recipe)
        db.session.commit()
        return new_recipe

