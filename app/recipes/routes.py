from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Recipe, Ingredient, RecipeIngredient, RecipeDietaryRestriction
from app import db
from sqlalchemy import or_

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/', methods=['GET'])
def get_recipes():
    category_id = request.args.get('category', type=int)
    dietary_id = request.args.get('dietary', type=int)
    search = request.args.get('search', '')
    
    query = Recipe.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    if dietary_id:
        query = query.join(RecipeDietaryRestriction).filter_by(dietary_restriction_id=dietary_id)
    if search:
        query = query.filter(or_(
            Recipe.title.ilike(f'%{search}%'),
            Recipe.description.ilike(f'%{search}%')
        ))
        
    recipes = query.all()
    return jsonify([{
        'recipe_id': r.recipe_id,
        'title': r.title,
        'description': r.description,
        'image_url': r.image_url,
        'author': r.author.username
    } for r in recipes])

@recipes_bp.route('/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Calculate average rating
    ratings = [r.rating for r in recipe.ratings]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    return jsonify({
        'recipe_id': recipe.recipe_id,
        'title': recipe.title,
        'description': recipe.description,
        'instructions': recipe.instructions,
        'image_url': recipe.image_url,
        'prep_time': recipe.prep_time,
        'cook_time': recipe.cook_time,
        'servings': recipe.servings,
        'author': {
            'user_id': recipe.author.user_id,
            'username': recipe.author.username
        },
        'category': {
            'category_id': recipe.category.category_id,
            'name': recipe.category.name
        } if recipe.category else None,
        'ingredients': [{
            'ingredient_id': ri.ingredient.ingredient_id,
            'name': ri.ingredient.name,
            'quantity': float(ri.quantity),
            'unit': ri.unit
        } for ri in recipe.ingredients],
        'dietary_restrictions': [{
            'dietary_restriction_id': dr.dietary_restriction_id,
            'name': dr.name
        } for dr in recipe.dietary_restrictions],
        'average_rating': round(avg_rating, 1),
        'ratings_count': len(ratings),
        'created_at': recipe.created_at,
        'updated_at': recipe.updated_at
    })

@recipes_bp.route('/', methods=['POST'])
@jwt_required()
def create_recipe():
    data = request.get_json()
    recipe = Recipe(
        user_id=get_jwt_identity(),
        title=data['title'],
        description=data['description'],
        instructions=data['instructions'],
        category_id=data['category_id'],
        image_url=data.get('image_url'),
        prep_time=data.get('prep_time'),
        cook_time=data.get('cook_time'),
        servings=data.get('servings')
    )
    
    db.session.add(recipe)
    db.session.commit()
    
    # Add ingredients
    for ing in data.get('ingredients', []):
        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe.recipe_id,
            ingredient_id=ing['ingredient_id'],
            quantity=ing['quantity'],
            unit=ing['unit']
        )
        db.session.add(recipe_ingredient)
    
    # Add dietary restrictions
    for dr_id in data.get('dietary_restrictions', []):
        rdr = RecipeDietaryRestriction(
            recipe_id=recipe.recipe_id,
            dietary_restriction_id=dr_id
        )
        db.session.add(rdr)
        
    db.session.commit()
    return jsonify({'message': 'Recipe created successfully', 'recipe_id': recipe.recipe_id}), 201

@recipes_bp.route('/<int:recipe_id>', methods=['PUT'])
@jwt_required()
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.get_json()
    for key in ['title', 'description', 'instructions', 'category_id', 'image_url', 
               'prep_time', 'cook_time', 'servings']:
        if key in data:
            setattr(recipe, key, data[key])
            
    db.session.commit()
    return jsonify({'message': 'Recipe updated successfully'})

@recipes_bp.route('/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != get_jwt_identity():
        return jsonify({'error': 'Unauthorized'}), 403
        
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe deleted successfully'}) 