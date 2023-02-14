from marshmallow import Schema, fields
from uuid import uuid4


class BaseTagSchema(Schema):
    id = fields.Str(dump_only=True)
    recipe_id = fields.Str(required=True)
    name = fields.Str(required=True)

class UpdateTagSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()

class BaseInstructionSchema(Schema):
    id = fields.Str(dump_only=True)
    details = fields.Str(required=True)
    recipe_id = fields.Str(required=True)

class UpdateInstructionSchema(Schema):
    id = fields.Str(dump_only=True)
    details = fields.Str()

    
class BaseIngredientSchema(Schema):
    id = fields.Str(dump_only=True)
    recipe_id = fields.Str(required=True)
    name = fields.Str(required=True)
    details = fields.Str()

class UpdateIngredientSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    details = fields.Str()

class BaseRecipeSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    ingredients = fields.List(required=True)
    instructions = fields.List(required=True)

class UpdateRecipeSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    ingredients = fields.List(BaseIngredientSchema())
    instructions = fields.List(BaseInstructionSchema())