import pytest
from app import create_app, db
from app.models import User
import os

@pytest.fixture
def client():
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    app = create_app()
    app.config['TESTING'] = True
    print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_register(client):
    response = client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'
    assert response.json['user']['username'] == 'testuser'
    assert response.json['user']['email'] == 'testuser@example.com'
    assert response.json['user']['profile_image'] is None

def test_register_missing_fields(client):
    response = client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Missing required fields'

def test_register_email_exists(client):
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    response = client.post('/api/register', json={
        'username': 'testuser2',
        'email': 'testuser@example.com',
        'password': 'testpassword2'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Email already registered'

def test_register_username_exists(client):
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    response = client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser2@example.com',
        'password': 'testpassword2'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Username already taken'