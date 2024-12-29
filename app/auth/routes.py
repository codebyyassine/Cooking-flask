from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import db
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    # Basic email validation pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_user_data(data, is_update=False):
    errors = []
    
    # Required fields for registration
    if not is_update:
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                errors.append(f"'{field}' is required")
    
    # Validate username
    if 'username' in data:
        if not isinstance(data['username'], str):
            errors.append("Username must be a string")
        elif len(data['username']) < 3:
            errors.append("Username must be at least 3 characters long")
        elif len(data['username']) > 50:
            errors.append("Username must be at most 50 characters long")
        elif not re.match(r'^[a-zA-Z0-9_]+$', data['username']):
            errors.append("Username can only contain letters, numbers, and underscores")
    
    # Validate email
    if 'email' in data:
        if not isinstance(data['email'], str):
            errors.append("Email must be a string")
        elif not validate_email(data['email']):
            errors.append("Invalid email format")
    
    # Validate password
    if 'password' in data:
        if not isinstance(data['password'], str):
            errors.append("Password must be a string")
        elif len(data['password']) < 8:
            errors.append("Password must be at least 8 characters long")
        elif not re.search(r'[A-Z]', data['password']):
            errors.append("Password must contain at least one uppercase letter")
        elif not re.search(r'[a-z]', data['password']):
            errors.append("Password must contain at least one lowercase letter")
        elif not re.search(r'\d', data['password']):
            errors.append("Password must contain at least one number")
    
    # Validate profile_image
    if 'profile_image' in data and data['profile_image'] is not None:
        if not isinstance(data['profile_image'], str):
            errors.append("Profile image must be a string URL")
        elif not data['profile_image'].startswith(('http://', 'https://')):
            errors.append("Profile image must be a valid URL starting with http:// or https://")
    
    return errors

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate input data
    validation_errors = validate_user_data(data)
    if validation_errors:
        return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
    
    # Check for existing email/username
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        profile_image=data.get('profile_image')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'profile_image': user.profile_image or None
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if not all(key in data for key in ['email', 'password']):
        return jsonify({'error': 'Email and password are required'}), 400
    
    if not isinstance(data['email'], str) or not isinstance(data['password'], str):
        return jsonify({'error': 'Email and password must be strings'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.user_id)
        return jsonify({
            'message': 'Login successful',
            'token': access_token,
            'user': {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'profile_image': user.profile_image or None
            }
        }), 200
        
    return jsonify({'error': 'Invalid email or password'}), 401

@auth_bp.route('/user/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    return jsonify({
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'profile_image': user.profile_image or None
    })

@auth_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'profile_image': user.profile_image or None
    })

@auth_bp.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    if user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate input data
    validation_errors = validate_user_data(data, is_update=True)
    if validation_errors:
        return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
        
    user = User.query.get_or_404(user_id)
    
    # Check for unique constraints
    if 'username' in data:
        if User.query.filter(User.user_id != user_id, User.username == data['username']).first():
            return jsonify({'error': 'Username already taken'}), 400
        user.username = data['username']
        
    if 'email' in data:
        if User.query.filter(User.user_id != user_id, User.email == data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        user.email = data['email']
        
    if 'profile_image' in data:
        user.profile_image = data['profile_image']
        
    if 'password' in data:
        user.set_password(data['password'])
        
    db.session.commit()
    
    return jsonify({
        'message': 'User updated successfully',
        'user': {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'profile_image': user.profile_image or None
        }
    }) 