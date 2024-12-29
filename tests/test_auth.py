import pytest
from app import create_app, db
from app.models import User
import os

@pytest.fixture
def client():
    os.environ['DATABASE_URL'] = 'sqlite:////tmp/test.db'
    app = create_app()
    app.config['TESTING'] = True
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
    user = User.query.filter_by(email='testuser@example.com').first()
    assert user is not None

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

def test_login(client):
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    response = client.post('/api/login', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Login successful'
    assert 'token' in response.json
    assert response.json['user']['username'] == 'testuser'
    assert response.json['user']['email'] == 'testuser@example.com'

def test_login_invalid_credentials(client):
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    response = client.post('/api/login', json={
        'email': 'testuser@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.json['error'] == 'Invalid email or password'

def test_get_current_user(client):
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    login_response = client.post('/api/login', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    token = login_response.json['token']
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/api/user/me', headers=headers)
    print(response.json)  # Print the response JSON for debugging
    assert response.status_code == 200
    assert response.json['username'] == 'testuser'
    assert response.json['email'] == 'testuser@example.com'

def test_get_user(client):
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    login_response = client.post('/api/login', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    token = login_response.json['token']
    headers = {'Authorization': f'Bearer {token}'}
    user_id = login_response.json['user']['user_id']
    response = client.get(f'/api/user/{user_id}', headers=headers)
    print(response.json)  # Print the response JSON for debugging
    assert response.status_code == 200
    assert response.json['username'] == 'testuser'
    assert response.json['email'] == 'testuser@example.com'

def test_update_user(client):
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    login_response = client.post('/api/login', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    token = login_response.json['token']
    headers = {'Authorization': f'Bearer {token}'}
    user_id = login_response.json['user']['user_id']
    response = client.put(f'/api/user/{user_id}', headers=headers, json={
        'username': 'updateduser',
        'email': 'updateduser@example.com',
        'profile_image': 'http://example.com/image.jpg',
        'password': 'updatedpassword'
    })
    print(response.json)  # Print the response JSON for debugging
    assert response.status_code == 200
    assert response.json['message'] == 'User updated successfully'
    assert response.json['user']['username'] == 'updateduser'
    assert response.json['user']['email'] == 'updateduser@example.com'
    assert response.json['user']['profile_image'] == 'http://example.com/image.jpg'

def test_get_user(client):
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    login_response = client.post('/api/login', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    token = login_response.json['token']
    headers = {'Authorization': f'Bearer {token}'}
    user_id = login_response.json['user']['user_id']
    response = client.get(f'/api/user/{user_id}', headers=headers)
    print(response.json)  # Print the response JSON for debugging
    assert response.status_code == 200
    assert response.json['username'] == 'testuser'
    assert response.json['email'] == 'testuser@example.com'

def test_update_user(client):
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    login_response = client.post('/api/login', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    token = login_response.json['token']
    headers = {'Authorization': f'Bearer {token}'}
    user_id = login_response.json['user']['user_id']
    response = client.put(f'/api/user/{user_id}', headers=headers, json={
        'username': 'updateduser',
        'email': 'updateduser@example.com',
        'profile_image': 'http://example.com/image.jpg',
        'password': 'updatedpassword'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'User updated successfully'
    assert response.json['user']['username'] == 'updateduser'
    assert response.json['user']['email'] == 'updateduser@example.com'
    assert response.json['user']['profile_image'] == 'http://example.com/image.jpg'

def test_subject_validation(client):
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    login_response = client.post('/api/login', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    token = login_response.json['token']
    headers = {'Authorization': f'Bearer {token}'}
    user_id = login_response.json['user']['user_id']
    response = client.put(f'/api/user/{user_id}', headers=headers, json={
        'username': 'updateduser',
        'email': 'updateduser@example.com',
        'profile_image': 'http://example.com/image.jpg',
        'password': 'updatedpassword',
        'subject': 'Test Subject'
    })
    assert response.status_code == 400
    assert 'error' in response.json