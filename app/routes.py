from flask import request, jsonify, Blueprint
from . import db
from .models import Meal
from .models import User
from .schemas import meal_schema, meals_schema
from .schemas import user_schema, users_schema
from .utils import calculate_tdee
from datetime import datetime

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
  return "Hello, world!"

@bp.route('/add_meal', methods=['POST'])
def add_meal():
    
    name = request.json['name']
    username = request.json['username']
    description = request.json.get('description', '')
    calories = request.json['calories']
    date = request.json.get('date', datetime.now().strftime('%Y-%m-%d'))

    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        return jsonify({"error": f"Username '{username}' does not exist. Please register first."}), 400

    new_meal = Meal(name=name, username=username, description=description, calories=calories, date=date)
    db.session.add(new_meal)
    db.session.commit()
    
    total_calories_consumed = db.session.query(db.func.sum(Meal.calories)).filter_by(username=username, date=date).scalar()
    
    if total_calories_consumed is None:
        total_calories_consumed = 0

    remaining_calories = existing_user.tdee - total_calories_consumed

    if remaining_calories > 0:
        message = "Meal added successfully."
    else:
        message = f"The daily TDEE has been surpassed by {abs(remaining_calories)} calories."
        remaining_calories = 0

    return jsonify({
        "message": message,
        "meal": meal_schema.dump(new_meal),
        "remaining_calories": remaining_calories
    })

@bp.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    return meals_schema.jsonify(meals)

@bp.route('/meals/<int:id>', methods=['GET'])
def get_meal(id):
    meal = Meal.query.get_or_404(id)
    return meal_schema.jsonify(meal)

@bp.route('/meals/<int:id>', methods=['PUT'])
def update_meal(id):
    meal = Meal.query.get_or_404(id)
    
    name = request.json['name']
    description = request.json.get('description', meal.description)
    calories = request.json['calories']
    date = request.json.get('date', meal.date)
    
    meal.name = name
    meal.description = description
    meal.calories = calories
    meal.date = date
    
    db.session.commit()
    
    return meal_schema.jsonify(meal)

@bp.route('/meals/<int:id>', methods=['DELETE'])
def delete_meal(id):
    meal = Meal.query.get_or_404(id)
    db.session.delete(meal)
    db.session.commit()
    
    return '', 204

@bp.route('/add_user', methods=['POST'])
def add_user():
    username = request.json['username']
    height = request.json['height']
    weight = request.json['weight']
    activity_level = request.json['activity_level']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": f"Username '{username}' already exists"}), 400

    # Calculate TDEE
    tdee = calculate_tdee(height, weight, activity_level)

    # Create a new user
    new_user = User(username=username, height=height, weight=weight, activity_level=activity_level, tdee=tdee)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@bp.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not found'}), 404
