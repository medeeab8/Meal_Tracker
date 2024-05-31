from flask import request, jsonify, Blueprint
from . import db
from .models import Meal
from .schemas import meal_schema, meals_schema

bp = Blueprint('routes', __name__)

@bp.route('/meals', methods=['POST'])
def add_meal():
    name = request.json['name']
    description = request.json.get('description', '')
    calories = request.json['calories']
    date = request.json.get('date', datetime.utcnow().strftime('%Y-%m-%d'))
    
    new_meal = Meal(name=name, description=description, calories=calories, date=date)
    db.session.add(new_meal)
    db.session.commit()
    
    return meal_schema.jsonify(new_meal)

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

@bp.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not found'}), 404
