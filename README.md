# Cooking Half API Documentation

A Flask-based REST API for managing recipes, users, and related features.

## Setup

1. **Environment Setup**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd cooking-half

   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```bash
   # Start PostgreSQL and pgAdmin using Docker
   docker-compose up -d

   # Access pgAdmin
   URL: http://localhost:5050
   Email: admin@admin.com
   Password: admin
   ```

## API Endpoints

### Authentication

#### Register User
- **URL**: `/api/auth/register`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "profile_image": "string (optional)"
  }
  ```
- **Response**: 
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "user_id": "integer",
      "username": "string",
      "email": "string",
      "profile_image": "string (optional)"
    }
  }
  ```

#### Login
- **URL**: `/api/auth/login`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Login successful",
    "token": "string (JWT token)",
    "user": {
      "user_id": "integer",
      "username": "string",
      "email": "string",
      "profile_image": "string (optional)"
    }
  }
  ```

#### Get Current User
- **URL**: `/api/auth/user/me`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "user_id": "integer",
    "username": "string",
    "email": "string",
    "profile_image": "string (optional)"
  }
  ```

#### Update User Profile
- **URL**: `/api/auth/user/<user_id>`
- **Method**: `PUT`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "username": "string (optional)",
    "email": "string (optional)",
    "password": "string (optional)",
    "profile_image": "string (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "message": "User updated successfully",
    "user": {
      "user_id": "integer",
      "username": "string",
      "email": "string",
      "profile_image": "string (optional)"
    }
  }
  ```

### Recipe Management

#### Get All Recipes
- **URL**: `/api/recipes`
- **Method**: `GET`
- **Query Parameters**:
  - `category=<category_id>`: Filter by category
  - `dietary=<dietary_restriction_id>`: Filter by dietary restriction
  - `search=<query>`: Search recipes by title or description
- **Response**:
  ```json
  [
    {
      "recipe_id": "integer",
      "title": "string",
      "description": "string",
      "image_url": "string",
      "author": "string"
    }
  ]
  ```

#### Get Single Recipe
- **URL**: `/api/recipes/<recipe_id>`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "recipe_id": "integer",
    "title": "string",
    "description": "string",
    "instructions": "string",
    "image_url": "string",
    "prep_time": "integer",
    "cook_time": "integer",
    "servings": "integer",
    "author": {
      "user_id": "integer",
      "username": "string"
    },
    "category": {
      "category_id": "integer",
      "name": "string"
    },
    "ingredients": [
      {
        "ingredient_id": "integer",
        "name": "string",
        "quantity": "float",
        "unit": "string"
      }
    ],
    "dietary_restrictions": [
      {
        "dietary_restriction_id": "integer",
        "name": "string"
      }
    ],
    "average_rating": "float",
    "ratings_count": "integer",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
  ```

#### Create Recipe
- **URL**: `/api/recipes`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "instructions": "string",
    "category_id": "integer",
    "image_url": "string (optional)",
    "prep_time": "integer (optional)",
    "cook_time": "integer (optional)",
    "servings": "integer (optional)",
    "ingredients": [
      {
        "ingredient_id": "integer",
        "quantity": "float",
        "unit": "string"
      }
    ],
    "dietary_restrictions": ["integer"]
  }
  ```
- **Response**:
  ```json
  {
    "message": "Recipe created successfully",
    "recipe_id": "integer"
  }
  ```

#### Update Recipe
- **URL**: `/api/recipes/<recipe_id>`
- **Method**: `PUT`
- **Authentication**: Required (must be recipe owner)
- **Request Body**: Same as Create Recipe (all fields optional)
- **Response**:
  ```json
  {
    "message": "Recipe updated successfully"
  }
  ```

#### Delete Recipe
- **URL**: `/api/recipes/<recipe_id>`
- **Method**: `DELETE`
- **Authentication**: Required (must be recipe owner)
- **Response**:
  ```json
  {
    "message": "Recipe deleted successfully"
  }
  ```

### Comments

#### Add Comment
- **URL**: `/api/recipes/<recipe_id>/comments`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "content": "string"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Comment submitted successfully"
  }
  ```

#### Get Comments
- **URL**: `/api/recipes/<recipe_id>/comments`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
      "comment_id": "integer",
      "user": {
        "user_id": "integer",
        "username": "string"
      },
      "content": "string",
      "created_at": "timestamp"
    }
  ]
  ```

### Ratings

#### Add Rating
- **URL**: `/api/recipes/<recipe_id>/ratings`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "rating": "integer (1-5)"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Rating submitted successfully"
  }
  ```

#### Get Ratings
- **URL**: `/api/recipes/<recipe_id>/ratings`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "average_rating": "float",
    "number_of_ratings": "integer"
  }
  ```

### Favorites

#### Add to Favorites
- **URL**: `/api/recipes/<recipe_id>/favorites`
- **Method**: `POST`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "message": "Recipe favorited successfully"
  }
  ```

#### Get User's Favorites
- **URL**: `/api/user/me/favorites`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
  ```json
  [
    {
      "recipe_id": "integer",
      "title": "string",
      "description": "string",
      "image_url": "string"
    }
  ]
  ```

### Categories
- **URL**: `/api/categories`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
      "category_id": "integer",
      "name": "string"
    }
  ]
  ```

### Ingredients
- **URL**: `/api/ingredients`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
      "ingredient_id": "integer",
      "name": "string"
    }
  ]
  ```

### Dietary Restrictions
- **URL**: `/api/dietary-restrictions`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
      "dietary_restriction_id": "integer",
      "name": "string"
    }
  ]
  ```

## Error Responses

All error responses follow this format:
```json
{
  "error": "Error message describing the issue"
}
```

Common HTTP status codes:
- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found

## Database Schema

The application uses PostgreSQL with the following main tables:
- Users
- Recipes
- Categories
- Ingredients
- Recipe_Ingredients
- Dietary_Restrictions
- Recipe_Dietary_Restrictions
- Ratings
- Comments
- Favorites 