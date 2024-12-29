from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Favorite, Recipe
from app import db

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/me/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    current_user_id = get_jwt_identity()
    favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    return jsonify([{
        'recipe_id': f.recipe.recipe_id,
        'title': f.recipe.title,
        'description': f.recipe.description,
        'image_url': f.recipe.image_url
    } for f in favorites])

@favorites_bp.route('/recipes/<int:recipe_id>/favorites', methods=['POST'])
@jwt_required()
def add_favorite(recipe_id):
    # Verify recipe exists
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Check if already favorited
    current_user_id = get_jwt_identity()
    existing_favorite = Favorite.query.filter_by(
        user_id=current_user_id,
        recipe_id=recipe_id
    ).first()
    
    if existing_favorite:
        return jsonify({'error': 'Recipe already in favorites'}), 400
        
    favorite = Favorite(
        user_id=current_user_id,
        recipe_id=recipe_id
    )
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Recipe favorited successfully'})

@favorites_bp.route('/recipes/<int:recipe_id>/favorites', methods=['DELETE'])
@jwt_required()
def remove_favorite(recipe_id):
    # Verify recipe exists
    recipe = Recipe.query.get_or_404(recipe_id)
    
    current_user_id = get_jwt_identity()
    favorite = Favorite.query.filter_by(
        user_id=current_user_id,
        recipe_id=recipe_id
    ).first()
    
    if not favorite:
        return jsonify({'error': 'Recipe not in favorites'}), 404
        
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'message': 'Recipe removed from favorites'}) 