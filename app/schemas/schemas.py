from marshmallow import Schema, fields
from uuid import uuid4


class BaseInstructionSchema(Schema):
    id = fields.UUID(default=uuid4())
    
class BaseIngredientSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
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