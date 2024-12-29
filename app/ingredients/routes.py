from flask import Blueprint, jsonify
from app.models import Ingredient

ingredients_bp = Blueprint('ingredients', __name__)

@ingredients_bp.route('/', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    return jsonify([{
        'ingredient_id': i.ingredient_id,
        'name': i.name
    } for i in ingredients]) 