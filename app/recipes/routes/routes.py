from app.recipes import blp as recipe_blp
from flask_smorest import abort
from flask.views import MethodView
from flask import jsonify, url_for
import requests
from app.schemas import BaseRecipeSchema, UpdateRecipeSchema
from app.models import Recipe, Direction, Ingredient, Tag, recipe_tags
from app import db



# def property_list_update(new_object_list, existing_obj_list, exist_list_obj_property, existing_recipe, model_class, model_class_property):
#     for new_obj in new_object_list:
#         if new_obj in exist_list_obj_property:
#             new_object_list.pop(new_object_list.index(new_obj))
#             obj_index = exist_list_obj_property.index(new_obj)
#             existing_obj_list.pop(obj_index)
#             exist_list_obj_property.pop(obj_index)
#     len_existing = len(existing_obj_list)
#     len_new = len(new_object_list)
#     if len_existing > len_new:
#         for i in range(len_existing-len_new):
#             db.session.delete(existing_obj_list[0])
#             existing_obj_list.pop(0)
#     elif len_new > len_existing:
#         for i in range(len_new - len_existing):
#             create_obj = model_class(model_class_property=new_object_list[0], recipe_id=existing_recipe.id)
#             db.session.add(create_obj)
#             new_object_list.pop(0)
#     if len_new > 0:
#         for new_obj in new_object_list:
#             existing_obj_list[0].model_class_property = new_obj
#             db.session.add(existing_obj_list[0])
#             existing_obj_list.pop(0)
#         db.session.commit()

@recipe_blp.route("/recipe/<int:recipe_id>")
class RecipeView(MethodView):

    @recipe_blp.response(200, BaseRecipeSchema)
    def get(self, recipe_id):
        return Recipe.query.filter_by(id=recipe_id).first()
    
    @recipe_blp.response(201, BaseRecipeSchema)
    def delete(self, recipe_id):
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        db.session.delete(recipe_tags.query.filter_by(recipe_id=recipe_id).all())
        db.session.delete(Ingredient.query.filter_by(recipe_id=recipe_id).all())
        db.session.delete(recipe)
        return recipe
  
    @recipe_blp.arguments(UpdateRecipeSchema)
    @recipe_blp.response(201, UpdateRecipeSchema)
    def put(self, recipe_data, recipe_id):
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        if recipe_data.get('ingredients') != None:
            exist_ing = {k.details:k for k in recipe.ingredients}
            new_ing = [k['details'] for k in recipe_data['ingredients']]
            for i in new_ing:
                if exist_ing.get(i) != None:
                    exist_ing.pop(i)
                    new_ing.pop(i)
            for ing in exist_ing:
                requests.delete(url_for('Ingredients.IngredientView', ingredient_id=exist_ing[ing].id, _external=True))
                print("older:"+ing)
            for ing in new_ing:
                print(ing)
                payload = {
                    "details": ing,
                    "recipe_id": recipe.id
                }
                requests.post(url_for('Ingredients.AllIngredientView', _external=True), json=payload)
        if recipe_data.get('directions') != None:
            exist_dir = {k.details:k for k in recipe.directions}
            new_dir = [k['details'] for k in recipe_data['directions']]
            for i in new_dir:
                if exist_dir.get(i) != None:
                    exist_dir.pop(i)
                    new_dir.pop(i)
            for direct in exist_dir:
                requests.delete(url_for('Directions.DirectionView', direction_id=exist_dir[direct].id, _external=True))
            for direct in new_dir:
                payload = {
                    "details": direct,
                    "recipe_id": recipe.id
                }
                requests.post(url_for('Directions.AllDirectionView', _external=True), json=payload)
        db.session.commit()
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        return recipe

        



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

