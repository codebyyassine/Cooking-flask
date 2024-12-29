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
- **URL**: `/api/register`
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
    "message": "User registered successfully"
  }
  ```

#### Login
- **URL**: `/api/login`
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
    "access_token": "string"
  }
  ```

#### Get User Profile
- **URL**: `/api/user/<user_id>`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "user_id": "integer",
    "username": "string",
    "email": "string",
    "profile_image": "string",
    "created_at": "datetime"
  }
  ```

#### Update User Profile
- **URL**: `/api/user/<user_id>`
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
    "message": "User updated successfully"
  }
  ```

### Recipes

#### Get All Recipes
- **URL**: `/api/recipes`
- **Method**: `GET`
- **Query Parameters**:
  - `category` (integer, optional): Filter by category ID
  - `dietary` (integer, optional): Filter by dietary restriction ID
  - `search` (string, optional): Search in title and description
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
    "created_at": "datetime",
    "updated_at": "datetime"
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

### Categories

#### Get All Categories
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

#### Get All Ingredients
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

#### Get All Dietary Restrictions
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
    "message": "Rating added successfully"
  }
  ```

#### Get Recipe Ratings
- **URL**: `/api/recipes/<recipe_id>/ratings`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
      "rating_id": "integer",
      "user_id": "integer",
      "rating": "integer",
      "created_at": "datetime"
    }
  ]
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
    "message": "Comment added successfully"
  }
  ```

#### Get Recipe Comments
- **URL**: `/api/recipes/<recipe_id>/comments`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
      "comment_id": "integer",
      "user_id": "integer",
      "content": "string",
      "created_at": "datetime",
      "username": "string"
    }
  ]
  ```

### Favorites

#### Add to Favorites
- **URL**: `/api/recipes/<recipe_id>/favorites`
- **Method**: `POST`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "message": "Recipe added to favorites"
  }
  ```

#### Get User's Favorites
- **URL**: `/api/user/<user_id>/favorites`
- **Method**: `GET`
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

## Authentication

All endpoints marked with "Authentication: Required" need a JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Error Responses

All endpoints may return the following error responses:

- **400 Bad Request**:
  ```json
  {
    "error": "Error message describing the issue"
  }
  ```

- **401 Unauthorized**:
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

- **403 Forbidden**:
  ```json
  {
    "error": "Unauthorized"
  }
  ```

- **404 Not Found**:
  ```json
  {
    "error": "Resource not found"
  }
  ```

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

For detailed schema information, see `backend/db.sql`. 