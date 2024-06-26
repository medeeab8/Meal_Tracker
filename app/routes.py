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

# Route for adding a meal
@bp.route('/add_meal', methods=['POST'])
def add_meal():
    # Extract meal details from request JSON
    name = request.json['name']
    username = request.json['username']
    description = request.json.get('description', '')
    calories = request.json['calories']
    date = request.json.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    # Check if the user exists
    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        return jsonify({"error": f"Username '{username}' does not exist. Please register first."}), 400
    
    # Create a new meal
    new_meal = Meal(name=name, username=username, description=description, calories=calories, date=date)
    db.session.add(new_meal)
    db.session.commit()
    
    # Calculate total calories consumed by the user for the day
    total_calories_consumed = db.session.query(db.func.sum(Meal.calories)).filter_by(username=username, date=date).scalar()
    
    if total_calories_consumed is None:
        total_calories_consumed = 0
    
    # Calculate remaining calories based on TDEE
    remaining_calories = existing_user.tdee - total_calories_consumed
    
    # Determine message based on remaining calories
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

# Route for retrieving meals by username
@bp.route('/meals/<username>', methods=['GET'])
def get_meals(username): 
    # Fetch meals based on username if provided, otherwise fetch all meals
    if username:
        meals = Meal.query.filter_by(username=username).all()
    else:
        meals = Meal.query.all()

    # Check if meals list is empty and return an error if no meals are found
    if not meals:
        return jsonify({'message': 'No meals found'}), 404
    
    return meals_schema.jsonify(meals)

# Route for retrieving a single meal by ID
@bp.route('/get_meal/<int:id>', methods=['GET'])
def get_meal(id):
    # Retrieve meal by ID or return 404 if not found
    meal = Meal.query.get_or_404(id)
    return meal_schema.jsonify(meal)

# Route for updating a meal
@bp.route('/update_meal/<int:id>', methods=['PUT'])
def update_meal(id):
    # Retrieve meal by ID or return 404 if not found
    meal = Meal.query.get_or_404(id)

    json_data = request.json
    
    # Check if the user is authorized to update this meal
    if 'username' not in json_data or json_data['username'] != meal.username:
        return jsonify({"error": "You are not authorized to update this meal."}), 403
    
    # Update meal details if provided in the request
    if 'name' in json_data:
        meal.name = json_data['name']
    if 'username' in json_data:
        meal.username = json_data['username']
    if 'description' in json_data:
        meal.description = json_data['description']
    if 'calories' in json_data:
        meal.calories = json_data['calories']
    if 'date' in json_data:
        meal.date = json_data['date']
    
    # Check if the user exists
    existing_user = User.query.filter_by(username=meal.username).first()
    if not existing_user:
        return jsonify({"error": f"Username '{meal.username}' does not exist. Please register first."}), 400
    
    # Commit changes to the database
    db.session.commit()
    # Return the updated meal
    return meal_schema.jsonify(meal)

# Route for deleting a meal by ID
@bp.route('/meals/<int:id>', methods=['DELETE'])
def delete_meal(id):
    # Retrieve meal by ID or return 404 if not found
    meal = Meal.query.get_or_404(id)
    # Delete the meal from the database
    db.session.delete(meal)
    db.session.commit()
    # Return message with 204 status code
    return jsonify({'message': 'Meal successfully deleted'}), 204

# Route for adding a user
@bp.route('/add_user', methods=['POST'])
def add_user():
    # Extract user details from request JSON
    username = request.json['username']
    height = request.json['height']
    weight = request.json['weight']
    activity_level = request.json['activity_level']
    
    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": f"Username '{username}' already exists"}), 400

    # Calculate TDEE
    tdee = calculate_tdee(height, weight, activity_level)

    # Create a new user
    new_user = User(username=username, height=height, weight=weight, activity_level=activity_level, tdee=tdee)

    # Commit changes to the database
    db.session.add(new_user)
    db.session.commit()

    # Returm user_schema
    return user_schema.jsonify(new_user)

# Route for updating a user by ID
@bp.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    # Retrieve the user by ID or return 404 if not found
    user = User.query.get_or_404(id)

    # Get JSON data from the request
    json_data = request.json
    tdee_reassession = False

    # Update user details if provided in the request
    if 'username' in json_data:
        user.username = json_data['username']
    if 'height' in json_data and user.height != json_data['height']:
        user.height = json_data['height']
        tdee_reassession = True
    if 'weight' in json_data and user.weight != json_data['weight']:
        user.weight = json_data['weight']
        tdee_reassession = True
    if 'activity_level' in json_data and user.activity_level != json_data['activity_level']:
        user.activity_level = json_data['activity_level']
        tdee_reassession = True

    # Reassess TDEE if any user details affecting TDEE are updated
    if tdee_reassession:
        tdee = calculate_tdee(user.height, user.weight, user.activity_level)
        user.tdee = tdee
        message = "TDEE was reassessed for this user!"
    else:
        message = "User updated successfully!"

    db.session.commit()

    # Return JSON response with the update message and user details
    return jsonify({
        "message":message,
        "user":user_schema.dump(user)})

# Route for deleting a user by ID
@bp.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    # Retrieve the user by ID or return 404 if not found
    user = User.query.get_or_404(id)
    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()
    # Return message with 204 status code
    return jsonify({'message': 'Meal successfully deleted'}), 204

# Error handler for 404 Not Found errors
@bp.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not found'}), 404
