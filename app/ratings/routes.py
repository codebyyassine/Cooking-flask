from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Rating
from app import db

ratings_bp = Blueprint('ratings', __name__)

@ratings_bp.route('/recipes/<int:recipe_id>/ratings', methods=['POST'])
@jwt_required()
def add_rating(recipe_id):
    data = request.get_json()
    rating = Rating(
        user_id=get_jwt_identity(),
        recipe_id=recipe_id,
        rating=data['rating']
    )
    db.session.add(rating)
    db.session.commit()
    return jsonify({'message': 'Rating added successfully'})

@ratings_bp.route('/recipes/<int:recipe_id>/ratings', methods=['GET'])
def get_ratings(recipe_id):
    ratings = Rating.query.filter_by(recipe_id=recipe_id).all()
    return jsonify([{
        'rating_id': r.rating_id,
        'user_id': r.user_id,
        'rating': r.rating,
        'created_at': r.created_at
    } for r in ratings]) 