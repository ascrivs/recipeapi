from app.ingredients import blp as ingredient_blp
from flask_smorest import abort
from flask.views import MethodView
from app.schemas import BaseIngredientSchema, UpdateIngredientSchema
from app.models import Ingredient
from app import db


@ingredient_blp.route("/ingredient/<int:ingredient_id>")
class IngredientView(MethodView):

    @ingredient_blp.response(200, BaseIngredientSchema)
    def get(self, ingredient_id):
        ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
        if ingredient != None:
            return ingredient
        else:
            abort(404,message="Ingredient not found.")
    
    @ingredient_blp.arguments(UpdateIngredientSchema)
    @ingredient_blp.response(201, BaseIngredientSchema)
    def put(self, ingredient_data, ingredient_id):
        updated_ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
        updated_ingredient.details = ingredient_data['details']
        db.session.add(updated_ingredient)
        db.session.commit()
        return updated_ingredient

    @ingredient_blp.response(200, UpdateIngredientSchema)
    def delete(self, ingredient_id):
        ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
        db.session.delete(ingredient)
        db.session.commit()
        return ingredient



@ingredient_blp.route("/")
class AllIngredientView(MethodView):

    @ingredient_blp.response(200, BaseIngredientSchema(many=True))
    def get(self):
        ingredients = Ingredient.query.all()
        return ingredients

    @ingredient_blp.arguments(BaseIngredientSchema)
    @ingredient_blp.response(201, BaseIngredientSchema)
    def post(self, ingredient_data):
        new_ingredient = Ingredient(details=ingredient_data['details'], recipe_id=ingredient_data['recipe_id'])
        db.session.add(new_ingredient)
        db.session.commit()
        return new_ingredient