from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
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
    
    if not all(key in data for key in ['email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
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

import logging

@auth_bp.route('/user/me', methods=['GET'])
@jwt_required()
def get_current_user():
    logging.info(f"Request headers: {request.headers}")
    logging.info(f"Request data: {request.get_json()}")
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
    logging.info(f"Request headers: {request.headers}")
    logging.info(f"Request data: {request.get_json()}")
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
    logging.info(f"Request headers: {request.headers}")
    logging.info(f"Request data: {request.get_json()}")
    if user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 403
        
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'subject' in data:
        return jsonify({'error': 'Subject field is not allowed'}), 400
    
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