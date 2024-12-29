from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Comment, Recipe
from app import db

comments_bp = Blueprint('comments', __name__)

def validate_comment_data(data):
    errors = []
    
    if not data:
        errors.append("No data provided")
        return errors
        
    if 'content' not in data:
        errors.append("Content is required")
    elif not isinstance(data['content'], str):
        errors.append("Content must be a string")
    elif len(data['content'].strip()) == 0:
        errors.append("Content cannot be empty")
    elif len(data['content']) > 1000:  # Maximum comment length
        errors.append("Content must be less than 1000 characters")
        
    return errors

@comments_bp.route('/<int:recipe_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(recipe_id):
    # Verify recipe exists
    recipe = Recipe.query.get_or_404(recipe_id)
    
    data = request.get_json()
    validation_errors = validate_comment_data(data)
    if validation_errors:
        return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
        
    comment = Comment(
        user_id=get_jwt_identity(),
        recipe_id=recipe_id,
        content=data['content'].strip()
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment submitted successfully'})

@comments_bp.route('/<int:recipe_id>/comments', methods=['GET'])
def get_comments(recipe_id):
    # Verify recipe exists
    recipe = Recipe.query.get_or_404(recipe_id)
    
    comments = Comment.query.filter_by(recipe_id=recipe_id).order_by(Comment.created_at.desc()).all()
    return jsonify([{
        'comment_id': c.comment_id,
        'user': {
            'user_id': c.user.user_id,
            'username': c.user.username
        },
        'content': c.content,
        'created_at': c.created_at
    } for c in comments]) 