from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Rating
from app import db

ratings_bp = Blueprint('ratings', __name__)

@ratings_bp.route('/<int:recipe_id>/ratings', methods=['POST'])
@jwt_required()
def add_rating(recipe_id):
    data = request.get_json()
    if not isinstance(data.get('rating'), int) or not 1 <= data['rating'] <= 5:
        return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
        
    # Check if user already rated this recipe
    existing_rating = Rating.query.filter_by(
        user_id=get_jwt_identity(),
        recipe_id=recipe_id
    ).first()
    
    if existing_rating:
        existing_rating.rating = data['rating']
    else:
        rating = Rating(
            user_id=get_jwt_identity(),
            recipe_id=recipe_id,
            rating=data['rating']
        )
        db.session.add(rating)
    
    db.session.commit()
    return jsonify({'message': 'Rating submitted successfully'})

@ratings_bp.route('/<int:recipe_id>/ratings', methods=['GET'])
def get_ratings(recipe_id):
    ratings = Rating.query.filter_by(recipe_id=recipe_id).all()
    if not ratings:
        return jsonify({
            'average_rating': 0,
            'number_of_ratings': 0
        })
    
    total_ratings = len(ratings)
    average_rating = sum(r.rating for r in ratings) / total_ratings
    
    return jsonify({
        'average_rating': round(average_rating, 1),
        'number_of_ratings': total_ratings
    }) 