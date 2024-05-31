import pytest
from app import create_app, db
from app.models import Meal

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_get_meals(client):
    response = client.get('/meals')
    assert response.status_code == 200

def test_add_meal(client):
    response = client.post('/add_meal', json={
        'name': 'Breakfast',
        'description': 'Eggs and toast',
        'calories': 350,
        'date': '2024-05-30'
    })
    assert response.status_code == 200
