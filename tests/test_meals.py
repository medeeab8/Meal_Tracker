import pytest
from app import create_app, db
from app.models import Meal, User
import json

@pytest.fixture
def client():
    # Create a Flask app instance for testing
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    # Create all database tables
    with app.app_context():
        db.create_all()
        yield client
        # Drop all database tables after testing 
        db.drop_all()

def test_get_meals_by_username(client):
    # Create a user and add to the database
    user = User(username='john_doe', height=175, weight=70, activity_level=2)
    db.session.add(user)
    db.session.commit()
    
    # Create meals for the user
    meal1 = Meal(name='Grilled Chicken Salad', username='john_doe', description='Grilled chicken breast with mixed greens and vinaigrette', calories=350, date='2024-06-02')
    meal2 = Meal(name='Pasta Carbonara', username='john_doe', description='Spaghetti with creamy sauce, bacon, and parmesan cheese', calories=600, date='2024-06-02')
    db.session.add(meal1)
    db.session.add(meal2)
    db.session.commit()

    # Test retrieving meals for the user
    response = client.get('/meals/john_doe')
    assert response.status_code == 200

    # Verify the retrieved meals
    meals = response.get_json()
    assert len(meals) == 2
    assert meals[0]['name'] == 'Grilled Chicken Salad'
    assert meals[1]['name'] == 'Pasta Carbonara'

    # Test retrieving meals for a nonexistent user
    response = client.get('/meals/nonexistent_user')
    assert response.status_code == 200

    # Verify no meals are retrieved for the nonexistent user
    meals = response.get_json()
    assert len(meals) == 0

def test_add_meal(client):
    # Create a test user and add to the database
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()

    # Data for the meal to be added
    meal_data = {
        'name': 'Chicken Salad',
        'username': 'testuser',
        'description': 'Grilled chicken with mixed greens',
        'calories': 350,
        'date': '2024-05-31'
    }
    # Test adding the meal
    response = client.post('/add_meal', data=json.dumps(meal_data), content_type='application/json')

    # Verify the response
    assert response.status_code == 200
    response_data = json.loads(response.data)

    assert 'Meal added successfully.' in response_data['message'] or 'The daily TDEE has been surpassed' in response_data['message']
    assert response_data['meal']['name'] == meal_data['name']
    assert response_data['meal']['username'] == meal_data['username']
    assert response_data['meal']['description'] == meal_data['description']
    assert response_data['meal']['calories'] == meal_data['calories']
    assert response_data['meal']['date'] == meal_data['date']
    assert 'remaining_calories' in response_data

def test_add_meal_user_not_exist(client):
    # Data for a meal with a non-existent user
    meal_data = {
        'name': 'Chicken Salad',
        'username': 'nonexistentuser',
        'description': 'Grilled chicken with mixed greens',
        'calories': 350,
        'date': '2024-05-31'
    }
    # Test adding the meal
    response = client.post('/add_meal', data=json.dumps(meal_data), content_type='application/json')
    
    # Verify the response
    assert response.status_code == 400
    response_data = json.loads(response.data)

    assert response_data['error'] == "Username 'nonexistentuser' does not exist. Please register first."


def test_get_meal(client):
    # Create a user and a meal for testing
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()

    test_meal = Meal(name='Dinner', username='testuser', description='Steak and potatoes', calories=600, date='2024-05-30')
    db.session.add(test_meal)
    db.session.commit()

    # Test retrieving the meal 
    response = client.get(f'/get_meal/{test_meal.id}')

    # Verify respose
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['name'] == 'Dinner'
    assert response_data['description'] == 'Steak and potatoes'
    assert response_data['calories'] == 600
    assert response_data['date'] == '2024-05-30'

def test_update_meal(client):
    # Create a user and a meal for testing
    user = User(username='john_doe', height=175, weight=70, activity_level=2)
    db.session.add(user)
    db.session.commit()

    meal = Meal(name='Grilled Chicken Salad', username='john_doe', description='Grilled chicken breast with mixed greens', calories=350, date='2024-06-02')
    db.session.add(meal)
    db.session.commit()

    # Test updating the meal
    response = client.put(f'/update_meal/{meal.id}', json={
        'username': 'john_doe',
        'name': 'Updated Chicken Salad',
        'description': 'Updated description',
        'calories': 400,
        'date': '2024-06-03'
    })
    assert response.status_code == 200

    # Verify the response
    updated_meal = response.get_json()
    assert updated_meal['name'] == 'Updated Chicken Salad'
    assert updated_meal['description'] == 'Updated description'
    assert updated_meal['calories'] == 400
    assert updated_meal['date'] == '2024-06-03'

    # Test updating the meal with unauthorized user
    response = client.put(f'/update_meal/{meal.id}', json={
        'username': 'jane_doe',
        'name': 'Unauthorized Update'
    })
    assert response.status_code == 403
    error_message = response.get_json()
    assert error_message['error'] == 'You are not authorized to update this meal.'

    # Test updating the meal with a non-existent user
    response = client.put(f'/update_meal/{meal.id}', json={
        'username': 'non_existent_user',
        'name': 'Update with non-existent user'
    })
    assert response.status_code == 403
    error_message = response.get_json()
    assert error_message['error'] == 'You are not authorized to update this meal.'

def test_delete_meal(client):
    # Create a test user and a meal for testing
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()

    test_meal = Meal(name='Dinner', username='testuser', description='Steak and potatoes', calories=600, date='2024-05-30')
    db.session.add(test_meal)
    db.session.commit()

    # Test deleting the meal
    response = client.delete(f'/meals/{test_meal.id}')

    # Verify the response
    assert response.status_code == 204
    assert Meal.query.get(test_meal.id) is None

def test_add_user(client):
    # Data for adding a new user
    user_data = {
        'username': 'newuser',
        'height': 170,
        'weight': 70,
        'activity_level': 3
    }

    # Test adding the user
    response = client.post('/add_user', data=json.dumps(user_data), content_type='application/json')
    
    # Verify the response
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['username'] == 'newuser'
    assert response_data['height'] == 170
    assert response_data['weight'] == 70
    assert response_data['activity_level'] == 3
    assert 'tdee' in response_data

def test_add_user_existing_username(client):
    # Create a test user with an existing username
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()
    
    # Data for adding a new user with the same username
    user_data = {
        'username': 'testuser',
        'height': 170,
        'weight': 70,
        'activity_level': 3
    }
  
    # Test adding the user
    response = client.post('/add_user', data=json.dumps(user_data), content_type='application/json')
    
    # Verify the response
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data['error'] == "Username 'testuser' already exists"



def test_update_user(client):
    # Create a test user
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()
    
    # Data for updating the user
    update_data = {
        'username': 'updateduser',
        'height': 175,
        'weight': 72,
        'activity_level': 4
    }
    
    # Test updating the user
    response = client.put(f'/update_user/{test_user.id}', data=json.dumps(update_data), content_type='application/json')
    
    # Verify the response
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['user']['username'] == 'updateduser'
    assert response_data['user']['height'] == 175
    assert response_data['user']['weight'] == 72
    assert response_data['user']['activity_level'] == 4
    assert response_data['message'] == "TDEE was reassessed for this user!"
    assert 'tdee' in response_data['user']

def test_update_user_no_tdee_reassessment(client):
    # Create a test user
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()

    # Data for updating the user without reassessing TDEE
    update_data = {
        'username': 'updateduser'
    }

    # Test updating the user
    response = client.put(f'/update_user/{test_user.id}', data=json.dumps(update_data), content_type='application/json')
    
    # Verify the response
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['user']['username'] == 'updateduser'
    assert response_data['message'] == "User updated successfully!"

def test_delete_user(client):
    # Create a test user
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()

    # Test deleting the user
    response = client.delete(f'/delete_user/{test_user.id}')

    # Verify the response
    assert response.status_code == 204
    assert User.query.get(test_user.id) is None