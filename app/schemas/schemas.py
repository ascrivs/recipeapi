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
    details = fields.Str()

class BaseRecipeSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    tags = fields.List(fields.Nested(UpdateTagSchema()))
    ingredients = fields.List(fields.Nested(UpdateIngredientSchema()))
    directions = fields.List(fields.Nested(UpdateInstructionSchema()))

class UpdateRecipeSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    tags = fields.List(fields.Nested(UpdateTagSchema()))
    ingredients = fields.List(fields.Nested(UpdateIngredientSchema()))
    instructions = fields.List(fields.Nested(UpdateInstructionSchema()))