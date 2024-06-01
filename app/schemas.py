from . import ma
from .models import Meal
from .models import User

class MealSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Meal

meal_schema = MealSchema()
meals_schema = MealSchema(many=True)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)