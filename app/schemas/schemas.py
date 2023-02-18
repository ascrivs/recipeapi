from marshmallow import Schema, fields
from uuid import uuid4


class BaseTagSchema(Schema):
    id = fields.Str(dump_only=True)
    recipe_id = fields.Str(required=True)
    name = fields.Str(required=True)

class UpdateTagSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()

class BaseDirectionSchema(Schema):
    id = fields.Str(dump_only=True)
    details = fields.Str(required=True)
    recipe_id = fields.Int(required=True)

class UpdateDirectionSchema(Schema):
    id = fields.Int(dump_only=True)
    details = fields.Str()

    
class BaseIngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    recipe_id = fields.Int(required=True)
    details = fields.Str()

class UpdateIngredientSchema(Schema):
    id = fields.Int(dump_only=True)
    details = fields.Str()

class BaseRecipeSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    tags = fields.List(fields.Nested(UpdateTagSchema()))
    ingredients = fields.List(fields.Nested(UpdateIngredientSchema()))
    directions = fields.List(fields.Nested(UpdateDirectionSchema()))

class UpdateRecipeSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    tags = fields.List(fields.Nested(UpdateTagSchema()))
    ingredients = fields.List(fields.Nested(UpdateIngredientSchema()))
    directions = fields.List(fields.Nested(UpdateDirectionSchema()))

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)