from app.ingredients import blp as ingredient_blp
from flask_smorest import abort
from flask_jwt_extended import jwt_required, get_jwt
from flask.views import MethodView
from app.schemas import BaseIngredientSchema, UpdateIngredientSchema
from app.models import Ingredient, Recipe
from app import db


@ingredient_blp.route("/ingredient/<string:ingredient_id>")
class IngredientView(MethodView):

    @ingredient_blp.response(200, BaseIngredientSchema)
    def get(self, ingredient_id):
        ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
        if ingredient != None:
            return ingredient
        else:
            abort(404,message="Ingredient not found.")
    
    @jwt_required(fresh=True)
    @ingredient_blp.arguments(UpdateIngredientSchema)
    @ingredient_blp.response(201, BaseIngredientSchema)
    def put(self, ingredient_data, ingredient_id):
        jwt = get_jwt()
        updated_ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
        if jwt["id"] == Recipe.query.filter_by(id=updated_ingredient.recipe_id).first().created_by:
            if updated_ingredient == None:
                abort(404, message="Ingredient not found.")
            updated_ingredient.details = ingredient_data['details']
            db.session.add(updated_ingredient)
            db.session.commit()
            return updated_ingredient
        else:
            abort(403, message="You must be the owner of the recipe or an administrator to modify")

    @jwt_required(fresh=True)
    @ingredient_blp.response(200, UpdateIngredientSchema)
    def delete(self, ingredient_id):
        jwt = get_jwt()
        updated_ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
        if jwt["id"] == Recipe.query.filter_by(id=updated_ingredient.recipe_id).first().created_by:
            ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
            db.session.delete(ingredient)
            db.session.commit()
            return ingredient
        else:
            abort(403, message="You must be the owner of the recipe or an administrator to modify")




@ingredient_blp.route("/")
class AllIngredientView(MethodView):

    @ingredient_blp.response(200, BaseIngredientSchema(many=True))
    def get(self):
        ingredients = Ingredient.query.all()
        return ingredients

    @jwt_required()
    @ingredient_blp.arguments(BaseIngredientSchema)
    @ingredient_blp.response(201, BaseIngredientSchema)
    def post(self, ingredient_data):
        jwt = get_jwt()
        if jwt["id"] == Recipe.query.filter_by(id=ingredient_data["recipe_id"]).first().created_by:
            new_ingredient = Ingredient(details=ingredient_data['details'], recipe_id=ingredient_data['recipe_id'])
            db.session.add(new_ingredient)
            db.session.commit()
            return new_ingredient
        else:
            abort(403, message="You must be the owner of the recipe or an administrator to modify")
