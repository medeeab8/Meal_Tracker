from . import ma
from .models import Meal

class MealSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Meal

meal_schema = MealSchema()
meals_schema = MealSchema(many=True)