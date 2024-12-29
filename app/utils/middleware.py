from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
                
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid or expired token'}), 401
            
    return decorated

def owner_required(model):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            
            # Get the object ID from kwargs
            object_id = kwargs.get(f'{model.__tablename__[:-1]}_id')
            if not object_id:
                return jsonify({'error': 'Invalid request'}), 400
                
            # Get the object
            obj = model.query.get(object_id)
            if not obj:
                return jsonify({'error': f'{model.__name__} not found'}), 404
                
            # Check ownership
            if not hasattr(obj, 'user_id') or obj.user_id != current_user_id:
                return jsonify({'error': 'Unauthorized access'}), 403
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator 