import pytest
from app import create_app, db
from app.models import Meal, User
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_get_meals_by_username(client):
    user = User(username='john_doe', height=175, weight=70, activity_level=2)
    db.session.add(user)
    db.session.commit()

    meal1 = Meal(name='Grilled Chicken Salad', username='john_doe', description='Grilled chicken breast with mixed greens and vinaigrette', calories=350, date='2024-06-02')
    meal2 = Meal(name='Pasta Carbonara', username='john_doe', description='Spaghetti with creamy sauce, bacon, and parmesan cheese', calories=600, date='2024-06-02')
    db.session.add(meal1)
    db.session.add(meal2)
    db.session.commit()

    response = client.get('/meals/john_doe')
    assert response.status_code == 200

    meals = response.get_json()
    assert len(meals) == 2
    assert meals[0]['name'] == 'Grilled Chicken Salad'
    assert meals[1]['name'] == 'Pasta Carbonara'

    response = client.get('/meals/nonexistent_user')
    assert response.status_code == 200

    meals = response.get_json()
    assert len(meals) == 0

def test_add_meal(client):
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()

    meal_data = {
        'name': 'Chicken Salad',
        'username': 'testuser',
        'description': 'Grilled chicken with mixed greens',
        'calories': 350,
        'date': '2024-05-31'
    }

    response = client.post('/add_meal', data=json.dumps(meal_data), content_type='application/json')

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
    meal_data = {
        'name': 'Chicken Salad',
        'username': 'nonexistentuser',
        'description': 'Grilled chicken with mixed greens',
        'calories': 350,
        'date': '2024-05-31'
    }

    response = client.post('/add_meal', data=json.dumps(meal_data), content_type='application/json')

    assert response.status_code == 400
    response_data = json.loads(response.data)

    assert response_data['error'] == "Username 'nonexistentuser' does not exist. Please register first."


def test_get_meal(client):
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()

    test_meal = Meal(name='Dinner', username='testuser', description='Steak and potatoes', calories=600, date='2024-05-30')
    db.session.add(test_meal)
    db.session.commit()

    response = client.get(f'/get_meal/{test_meal.id}')

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['name'] == 'Dinner'
    assert response_data['description'] == 'Steak and potatoes'
    assert response_data['calories'] == 600
    assert response_data['date'] == '2024-05-30'

def test_update_meal(client):
    user = User(username='john_doe', height=175, weight=70, activity_level=2)
    db.session.add(user)
    db.session.commit()

    meal = Meal(name='Grilled Chicken Salad', username='john_doe', description='Grilled chicken breast with mixed greens', calories=350, date='2024-06-02')
    db.session.add(meal)
    db.session.commit()

    response = client.put(f'/update_meal/{meal.id}', json={
        'username': 'john_doe',
        'name': 'Updated Chicken Salad',
        'description': 'Updated description',
        'calories': 400,
        'date': '2024-06-03'
    })
    assert response.status_code == 200

    updated_meal = response.get_json()
    assert updated_meal['name'] == 'Updated Chicken Salad'
    assert updated_meal['description'] == 'Updated description'
    assert updated_meal['calories'] == 400
    assert updated_meal['date'] == '2024-06-03'

    response = client.put(f'/update_meal/{meal.id}', json={
        'username': 'jane_doe',
        'name': 'Unauthorized Update'
    })
    assert response.status_code == 403
    error_message = response.get_json()
    assert error_message['error'] == 'You are not authorized to update this meal.'

    response = client.put(f'/update_meal/{meal.id}', json={
        'username': 'non_existent_user',
        'name': 'Update with non-existent user'
    })
    assert response.status_code == 403
    error_message = response.get_json()
    assert error_message['error'] == 'You are not authorized to update this meal.'

def test_delete_meal(client):
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()

    test_meal = Meal(name='Dinner', username='testuser', description='Steak and potatoes', calories=600, date='2024-05-30')
    db.session.add(test_meal)
    db.session.commit()

    response = client.delete(f'/meals/{test_meal.id}')

    assert response.status_code == 204
    assert Meal.query.get(test_meal.id) is None

def test_add_user(client):
    user_data = {
        'username': 'newuser',
        'height': 170,
        'weight': 70,
        'activity_level': 3
    }

    response = client.post('/add_user', data=json.dumps(user_data), content_type='application/json')

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['username'] == 'newuser'
    assert response_data['height'] == 170
    assert response_data['weight'] == 70
    assert response_data['activity_level'] == 3
    assert 'tdee' in response_data

def test_add_user_existing_username(client):
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()

    user_data = {
        'username': 'testuser',
        'height': 170,
        'weight': 70,
        'activity_level': 3
    }

    response = client.post('/add_user', data=json.dumps(user_data), content_type='application/json')

    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data['error'] == "Username 'testuser' already exists"



def test_update_user(client):
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()

    update_data = {
        'username': 'updateduser',
        'height': 175,
        'weight': 72,
        'activity_level': 4
    }

    response = client.put(f'/update_user/{test_user.id}', data=json.dumps(update_data), content_type='application/json')

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['user']['username'] == 'updateduser'
    assert response_data['user']['height'] == 175
    assert response_data['user']['weight'] == 72
    assert response_data['user']['activity_level'] == 4
    assert response_data['message'] == "TDEE was reassessed for this user!"
    assert 'tdee' in response_data['user']

def test_update_user_no_tdee_reassessment(client):
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()

    update_data = {
        'username': 'updateduser'
    }

    response = client.put(f'/update_user/{test_user.id}', data=json.dumps(update_data), content_type='application/json')

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['user']['username'] == 'updateduser'
    assert response_data['message'] == "User updated successfully!"

def test_delete_user(client):
    test_user = User(username='testuser', height=180, weight=75, activity_level=3, tdee=2500)
    db.session.add(test_user)
    db.session.commit()

    response = client.delete(f'/delete_user/{test_user.id}')

    assert response.status_code == 204
    assert User.query.get(test_user.id) is None