from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Comment
from app import db

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/recipes/<int:recipe_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(recipe_id):
    data = request.get_json()
    comment = Comment(
        user_id=get_jwt_identity(),
        recipe_id=recipe_id,
        content=data['content']
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully'})

@comments_bp.route('/recipes/<int:recipe_id>/comments', methods=['GET'])
def get_comments(recipe_id):
    comments = Comment.query.filter_by(recipe_id=recipe_id).all()
    return jsonify([{
        'comment_id': c.comment_id,
        'user_id': c.user_id,
        'content': c.content,
        'created_at': c.created_at,
        'username': c.user.username
    } for c in comments]) 