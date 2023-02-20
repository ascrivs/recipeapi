from app.recipes import blp as recipe_blp
from flask_smorest import abort
from flask.views import MethodView
from flask import url_for, request
from flask_jwt_extended import jwt_required, get_jwt
import requests
from app.schemas import BaseRecipeSchema, UpdateRecipeSchema
from app.models import Recipe, Direction, Ingredient, Tag, recipe_tags, User
from app import db, jwt as app_jwt_mgr


@recipe_blp.route("/recipe/<string:recipe_id>")
class RecipeView(MethodView):

    @recipe_blp.response(200, BaseRecipeSchema)
    def get(self, recipe_id):
        return Recipe.query.filter_by(id=recipe_id).first()
    
    @jwt_required()
    @recipe_blp.response(201, BaseRecipeSchema)
    def delete(self, recipe_id):
        jwt = get_jwt()
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        if jwt.get('id') == recipe.created_by or jwt.get('role') == 'administrator':
            db.session.delete(recipe_tags.query.filter_by(recipe_id=recipe_id).all())
            db.session.delete(Ingredient.query.filter_by(recipe_id=recipe_id).all())
            db.session.delete(recipe)
            return recipe
        abort(403, message="Access denied.")
  
    @jwt_required()
    @recipe_blp.arguments(UpdateRecipeSchema)
    @recipe_blp.response(201, UpdateRecipeSchema)
    def put(self, recipe_data, recipe_id):
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        jwt = get_jwt()
        request_head = request.headers.get('Authorization')
        head = {'Authorization': request_head}
        if jwt.get('id') == recipe.created_by:
            if recipe_data.get('name') != None:
                recipe.name = recipe_data['name']
            if recipe_data.get('description') != None:
                recipe.description = recipe_data['description']
            if recipe_data.get('ingredients') != None:
                exist_ing = {k.details:k for k in recipe.ingredients}
                new_ing = [k['details'] for k in recipe_data['ingredients']]
                for i in new_ing:
                    if exist_ing.get(i) != None:
                        exist_ing.pop(i)
                        new_ing.pop(new_ing.index(i))
                for ing in exist_ing:
                    requests.delete(url_for('Ingredients.IngredientView', ingredient_id=exist_ing[ing].id, _external=True), headers=head)
                for ing in new_ing:
                    payload = {
                        "details": ing,
                        "recipe_id": recipe.id
                    }
                    requests.post(url_for('Ingredients.AllIngredientView', _external=True), json=payload, headers=head)
            if recipe_data.get('directions') != None:
                exist_dir = {k.details:k for k in recipe.directions}
                new_dir = [k['details'] for k in recipe_data['directions']]
                for i in new_dir:
                    if exist_dir.get(i) != None:
                        exist_dir.pop(i)
                        new_dir.pop(new_dir.index(i))
                for direct in exist_dir:
                    requests.delete(url_for('Directions.DirectionView', direct_id=exist_dir[direct].id, _external=True), headers=head)
                for direct in new_dir:
                    payload = {
                        "details": direct,
                        "recipe_id": recipe.id
                    }
                    requests.post(url_for('Directions.AllDirectionsView', _external=True), json=payload, headers=head)
            if recipe_data.get('tags') != None:
                exist_tags = {k.name:k for k in recipe.tags}
                new_tags = [k['name'].lower() for k in recipe_data['tags']]
                for i in new_tags:
                    if exist_tags.get(i) != None:
                        exist_tags.pop(i)
                        new_tags.pop(new_tags.index(i))
                for tag in exist_tags:
                    requests.delete(url_for('Recipes.RecipeTagView', tag_id=exist_tags[tag].id, recipe_id=recipe.id, _external=True), headers=head)
                for tag in new_tags:
                    record_tag = Tag.query.filter_by(name=tag).first()
                    if record_tag == None:
                        payload = {
                            "name": tag,
                        }
                        requests.post(url_for('Tags.AllTagsView', _external=True), json=payload, headers=head)
                    else:
                        recipe.tags.append(record_tag)



            db.session.commit()
            recipe = Recipe.query.filter_by(id=recipe_id).first()
            return recipe
        abort(403, message="Access denied. Please login.")



@recipe_blp.route("/")
class AllRecipesView(MethodView):

    @recipe_blp.response(200, BaseRecipeSchema(many=True))
    def get(self):
        recipes = Recipe.query.all()
        return recipes

    @jwt_required()
    @recipe_blp.arguments(BaseRecipeSchema)
    @recipe_blp.response(201, BaseRecipeSchema)
    def post(self, recipe):
        jwt = get_jwt()
        new_recipe = Recipe(name=recipe['name'],description=recipe['description'], created_by=jwt.get('id'))
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


@recipe_blp.route("/<string:recipe_id>/recipetag/<string:tag_id>")
class RecipeTagView(MethodView):

    @jwt_required()
    @recipe_blp.response(201, BaseRecipeSchema)
    def delete(self, recipe_id, tag_id):
        jwt = get_jwt()
        if jwt['id'] == Recipe.query.filter_by(id=recipe_id).first().created_by:
            recipe = Recipe.query.filter_by(id=recipe_id).first()
            recipe.tags.pop(recipe.tags.index(Tag.query.filter_by(id=tag_id).first()))
            db.session.commit()
            return recipe
        abort(403, message="Access denied.")
        