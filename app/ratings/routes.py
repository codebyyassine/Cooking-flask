from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Rating, Recipe
from app import db

ratings_bp = Blueprint('ratings', __name__)

def validate_rating_data(data):
    errors = []
    
    if not data:
        errors.append("No data provided")
        return errors
        
    if 'rating' not in data:
        errors.append("Rating is required")
    elif not isinstance(data.get('rating'), int):
        errors.append("Rating must be an integer")
    elif not 1 <= data['rating'] <= 5:
        errors.append("Rating must be between 1 and 5")
        
    return errors

@ratings_bp.route('/<int:recipe_id>/ratings', methods=['POST'])
@jwt_required()
def add_rating(recipe_id):
    # Verify recipe exists
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Verify user hasn't already rated this recipe
    current_user_id = get_jwt_identity()
    existing_rating = Rating.query.filter_by(
        user_id=current_user_id,
        recipe_id=recipe_id
    ).first()
    
    data = request.get_json()
    validation_errors = validate_rating_data(data)
    if validation_errors:
        return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
    
    if existing_rating:
        # Update existing rating
        existing_rating.rating = data['rating']
        message = "Rating updated successfully"
    else:
        # Create new rating
        rating = Rating(
            user_id=current_user_id,
            recipe_id=recipe_id,
            rating=data['rating']
        )
        db.session.add(rating)
        message = "Rating submitted successfully"
    
    db.session.commit()
    return jsonify({'message': message})

@ratings_bp.route('/<int:recipe_id>/ratings', methods=['GET'])
def get_ratings(recipe_id):
    # Verify recipe exists
    recipe = Recipe.query.get_or_404(recipe_id)
    
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