from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os
from dotenv import load_dotenv

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Load environment variables
    load_dotenv()

    # Initialize Flask app
    app = Flask(__name__)

    # Configure CORS
    CORS(app, 
         resources={r"/api/*": {
             "origins": ["http://localhost:5173", "http://localhost:3000"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
             "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
             "supports_credentials": True,
             "send_wildcard": False,
             "expose_headers": ["Content-Range", "X-Content-Range"],
             "max_age": 86400
         }})

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/cooking_half')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configure JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # Change in production
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    # Register blueprints
    from .auth.routes import auth_bp
    from .recipes.routes import recipes_bp
    from .categories.routes import categories_bp
    from .ingredients.routes import ingredients_bp
    from .ratings.routes import ratings_bp
    from .comments.routes import comments_bp
    from .favorites.routes import favorites_bp
    from .dietary_restrictions.routes import dietary_restrictions_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(recipes_bp, url_prefix='/api/recipes')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(ingredients_bp, url_prefix='/api/ingredients')
    app.register_blueprint(ratings_bp, url_prefix='/api/recipes')
    app.register_blueprint(comments_bp, url_prefix='/api/recipes')
    app.register_blueprint(favorites_bp, url_prefix='/api/user')
    app.register_blueprint(dietary_restrictions_bp, url_prefix='/api/dietary-restrictions')

    return app 