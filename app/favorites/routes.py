from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Favorite
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
    favorite = Favorite(
        user_id=get_jwt_identity(),
        recipe_id=recipe_id
    )
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Recipe favorited successfully'}) 