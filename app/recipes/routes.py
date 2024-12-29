from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Recipe, Ingredient, RecipeIngredient, RecipeDietaryRestriction
from app import db
from sqlalchemy import or_

recipes_bp = Blueprint('recipes', __name__)

def validate_recipe_data(data, is_update=False):
    errors = []
    
    # Required fields for creation
    if not is_update:
        required_fields = ['title', 'description', 'instructions', 'category_id']
        for field in required_fields:
            if field not in data:
                errors.append(f"'{field}' is required")
    
    # Validate field types and constraints
    if 'title' in data and (not isinstance(data['title'], str) or len(data['title']) > 200):
        errors.append("Title must be a string with maximum length of 200 characters")
    
    if 'description' in data and not isinstance(data['description'], str):
        errors.append("Description must be a string")
        
    if 'instructions' in data and not isinstance(data['instructions'], str):
        errors.append("Instructions must be a string")
        
    if 'category_id' in data and not isinstance(data['category_id'], int):
        errors.append("Category ID must be an integer")
        
    if 'prep_time' in data and (not isinstance(data['prep_time'], int) or data['prep_time'] < 0):
        errors.append("Prep time must be a positive integer")
        
    if 'cook_time' in data and (not isinstance(data['cook_time'], int) or data['cook_time'] < 0):
        errors.append("Cook time must be a positive integer")
        
    if 'servings' in data and (not isinstance(data['servings'], int) or data['servings'] <= 0):
        errors.append("Servings must be a positive integer")
        
    # Validate ingredients
    if 'ingredients' in data:
        if not isinstance(data['ingredients'], list):
            errors.append("Ingredients must be a list")
        else:
            for i, ing in enumerate(data['ingredients']):
                if not isinstance(ing, dict):
                    errors.append(f"Ingredient {i+1} must be an object")
                    continue
                    
                if 'ingredient_id' not in ing:
                    errors.append(f"Ingredient {i+1} missing 'ingredient_id'")
                elif not isinstance(ing['ingredient_id'], int):
                    errors.append(f"Ingredient {i+1} 'ingredient_id' must be an integer")
                    
                if 'quantity' not in ing:
                    errors.append(f"Ingredient {i+1} missing 'quantity'")
                elif not isinstance(ing['quantity'], (int, float)) or ing['quantity'] <= 0:
                    errors.append(f"Ingredient {i+1} 'quantity' must be a positive number")
                    
                if 'unit' not in ing:
                    errors.append(f"Ingredient {i+1} missing 'unit'")
                elif not isinstance(ing['unit'], str):
                    errors.append(f"Ingredient {i+1} 'unit' must be a string")
    
    # Validate dietary restrictions
    if 'dietary_restrictions' in data:
        if not isinstance(data['dietary_restrictions'], list):
            errors.append("Dietary restrictions must be a list of integers")
        else:
            for i, dr_id in enumerate(data['dietary_restrictions']):
                if not isinstance(dr_id, int):
                    errors.append(f"Dietary restriction ID at position {i+1} must be an integer")
    
    return errors

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
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    # Validate input data
    validation_errors = validate_recipe_data(data)
    if validation_errors:
        return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
    
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
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    # Validate input data
    validation_errors = validate_recipe_data(data, is_update=True)
    if validation_errors:
        return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
    
    # Update basic fields
    for key in ['title', 'description', 'instructions', 'category_id', 
               'image_url', 'prep_time', 'cook_time', 'servings']:
        if key in data:
            setattr(recipe, key, data[key])
            
    # Update ingredients if provided
    if 'ingredients' in data:
        # Remove existing ingredients
        RecipeIngredient.query.filter_by(recipe_id=recipe_id).delete()
        
        # Add new ingredients
        for ing in data['ingredients']:
            recipe_ingredient = RecipeIngredient(
                recipe_id=recipe_id,
                ingredient_id=ing['ingredient_id'],
                quantity=ing['quantity'],
                unit=ing['unit']
            )
            db.session.add(recipe_ingredient)
    
    # Update dietary restrictions if provided
    if 'dietary_restrictions' in data:
        # Remove existing restrictions
        RecipeDietaryRestriction.query.filter_by(recipe_id=recipe_id).delete()
        
        # Add new restrictions
        for dr_id in data['dietary_restrictions']:
            rdr = RecipeDietaryRestriction(
                recipe_id=recipe_id,
                dietary_restriction_id=dr_id
            )
            db.session.add(rdr)
            
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