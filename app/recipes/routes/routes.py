from app.recipes import blp as recipe_blp
from flask_smorest import abort
from flask.views import MethodView
from app.schemas import BaseRecipeSchema, UpdateRecipeSchema
from app.models import Recipe, Direction, Ingredient, Tag, recipe_tags
from app import db



def property_list_update(new_object_list, existing_obj_list, exist_list_obj_property, existing_recipe, model_class, model_class_property):
    for new_obj in new_object_list:
        if new_obj in exist_list_obj_property:
            new_object_list.pop(new_object_list.index(new_obj))
            obj_index = exist_list_obj_property.index(new_obj)
            existing_obj_list.pop(obj_index)
            exist_list_obj_property.pop(obj_index)
    len_existing = len(existing_obj_list)
    len_new = len(new_object_list)
    if len_existing > len_new:
        for i in range(len_existing-len_new):
            db.session.delete(existing_obj_list[0])
            existing_obj_list.pop(0)
    elif len_new > len_existing:
        for i in range(len_new - len_existing):
            create_obj = model_class(model_class_property=new_object_list[0], recipe_id=existing_recipe.id)
            db.session.add(create_obj)
            new_object_list.pop(0)
    if len_new > 0:
        for new_obj in new_object_list:
            existing_obj_list[0].model_class_property = new_obj
            db.session.add(existing_obj_list[0])
            existing_obj_list.pop(0)
        db.session.commit()

@recipe_blp.route("/recipe/<string:recipe_id>")
class RecipeView(MethodView):
    def get(self, recipe_id):
        return recipe_id
    
    @recipe_blp.response(201, BaseRecipeSchema)
    def delete(self, recipe_id):
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        db.session.delete(recipe_tags.query.filter_by(recipe_id=recipe_id).all())
        db.session.delete(Ingredient.query.filter_by(recipe_id=recipe_id).all())
        db.session.delete(recipe)
        return recipe
  
    @recipe_blp.arguments(UpdateRecipeSchema)
    @recipe_blp.response(201, UpdateRecipeSchema)
    def put(self, recipe_data):
        update_recipe = Recipe.query.filter_by(update_recipe['id']).first()
        if recipe_data.get('ingredients') != None:
            new_recipe_ingredients = [recipe_data['ingredients'][k]["details"] for k in recipe_data['ingredients']]
            existing_ingredients = update_recipe.ingredients
            existing_ingredients_details = [ingre.details for ingre in existing_ingredients]
            property_list_update(
                new_object_list=new_recipe_ingredients,
                existing_obj_list=existing_ingredients,
                exist_list_obj_property=existing_ingredients_details,
                existing_recipe=update_recipe,
                model_class=Ingredient,
                model_class_property=Ingredient.details
                )
        if recipe_data.get('directions') != None:
            new_recipe_directions = [recipe_data['directions'][k]["details"] for k in recipe_data['ingredients']]
            existing_directions = update_recipe.directions
            existing_directions_details = [directs.details for directs in existing_directions]
            property_list_update(
                new_object_list=new_recipe_directions,
                existing_obj_list=existing_directions,
                exist_list_obj_property=existing_directions_details,
                existing_recipe=update_recipe,
                model_class=Direction,
                model_class_property=Direction.details
                )
        if recipe_data.get('tags') != None:
            new_recipe_tags = [recipe_data['tags'][k]["name"] for k in recipe_data['tags']]
            existing_tags = update_recipe.tags
            existing_tags_name = [tag.name for tag in existing_tags]
            for new_tag in new_recipe_tags:
                if new_tag in existing_tags_name:
                    new_recipe_tags.pop(new_recipe_tags.index(new_tag))
                    tag_index = existing_tags_name.index(new_tag)
                    existing_tags.pop(tag_index)
                    existing_tags_name.pop(tag_index)
            for new_tag in new_recipe_tags:
                existing_tag = Tag.query.filter_by(name=new_tag) != None
                if existing_tag != None:
                    update_recipe.tags.append(existing_tag)
                else:
                    create_tag = Tag(name=new_tag)
                    db.session.add(create_tag)
                    update_recipe.tags.append(create_tag)

        #     for ingre in new_recipe_ingredients:
        #         if ingre in existing_ingredients_details:
        #             new_recipe_ingredients.pop(new_recipe_ingredients.index(ingre))
        #             detail_ind = existing_ingredients_details.index(ingre)
        #             existing_ingredients.pop(detail_ind)
        #             existing_ingredients_details.pop(detail_ind)
        #     len_existing = len(existing_ingredients)
        #     len_new = len(new_recipe_ingredients)
        #     if len_existing > len_new:
        #         for i in range(len_existing-len_new):
        #             db.session.delete(existing_ingredients[0])
        #             existing_ingredients.pop(0)
        #     elif len_new > len_existing:
        #         for i in range(len_new - len_existing):
        #             new_ing = Ingredient(details=new_recipe_ingredients[0], recipe_id=update_recipe.id)
        #             db.session.add(new_ing)
        #             new_recipe_ingredients.pop(0)
        #     if len_new > 0:
        #         for new_i in new_recipe_ingredients:
        #             existing_ingredients[0].details = new_i
        #             db.session.add(existing_ingredients[0])
        #             existing_ingredients.pop(0)
        #     ############
        # if recipe_data.get('directions') != None:
        #     new_recipe_directions = [recipe_data['directions'][k]["details"] for k in recipe_data['ingredients']]
        #     existing_directions = update_recipe.directions
        #     existing_directions_details = [directs.details for directs in existing_directions]
        #     for directs in new_recipe_directions:
        #         if directs in existing_directions_details:
        #             new_recipe_directions.pop(new_recipe_directions.index(directs))
        #             detail_directs = existing_directions_details.index(directs)
        #             existing_directions.pop(detail_ind)
        #             existing_directions_details.pop(detail_ind)
        #     len_existing = len(existing_directions)
        #     len_new = len(new_recipe_directions)
        #     if len_existing > len_new:
        #         for i in range(len_existing-len_new):
        #             db.session.delete(existing_directions[0])
        #             existing_directions.pop(0)
        #     elif len_new > len_existing:
        #         for i in range(len_new - len_existing):
        #             new_directs = Direction(details=new_recipe_directions[0], recipe_id=update_recipe.id)
        #             db.session.add(new_directs)
        #             new_recipe_directions.pop(0)
        #     if len_new > 0:
        #         for new_d in new_recipe_ingredients:
        #             existing_directions[0].details = new_d
        #             db.session.add(existing_directions[0])
        #             existing_directions.pop(0)
    

            



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

