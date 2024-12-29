from flask import Blueprint, jsonify
from app.models import Category

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'category_id': c.category_id,
        'name': c.name
    } for c in categories]) 