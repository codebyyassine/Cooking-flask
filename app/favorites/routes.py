from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Favorite
from app import db

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/recipes/<int:recipe_id>/favorites', methods=['POST'])
@jwt_required()
def add_favorite(recipe_id):
    favorite = Favorite(
        user_id=get_jwt_identity(),
        recipe_id=recipe_id
    )
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Recipe added to favorites'})

@favorites_bp.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'recipe_id': f.recipe_id,
        'title': f.recipe.title,
        'description': f.recipe.description,
        'image_url': f.recipe.image_url
    } for f in favorites]) 