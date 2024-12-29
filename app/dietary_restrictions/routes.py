from flask import Blueprint, jsonify
from app.models import DietaryRestriction

dietary_restrictions_bp = Blueprint('dietary_restrictions', __name__)

@dietary_restrictions_bp.route('/', methods=['GET'])
def get_dietary_restrictions():
    restrictions = DietaryRestriction.query.all()
    return jsonify([{
        'dietary_restriction_id': r.dietary_restriction_id,
        'name': r.name
    } for r in restrictions]) 