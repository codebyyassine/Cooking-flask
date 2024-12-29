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
- **Content-Type**: `multipart/form-data` or `application/json`
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "profile_image": "file (optional)"
  }
  ```
- **Validation Rules**:
  - Username:
    - Required
    - 3-50 characters long
    - Can only contain letters, numbers, and underscores
  - Email:
    - Required
    - Must be a valid email format
  - Password:
    - Required
    - Minimum 8 characters
    - Must contain at least one uppercase letter
    - Must contain at least one lowercase letter
    - Must contain at least one number
  - Profile Image:
    - Optional
    - Must be an image file (PNG, JPG, JPEG, GIF)
    - Maximum file size: 5MB
    - Will be optimized and resized if necessary
- **Response**: 
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "user_id": "integer",
      "username": "string",
      "email": "string",
      "profile_image": "string (URL)"
    }
  }
  ```

#### Update Profile Image
- **URL**: `/api/auth/user/me/profile-image`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Authentication**: Required
- **Request Body**:
  ```
  profile_image: file
  ```
- **Validation Rules**:
  - Required
  - Must be an image file (PNG, JPG, JPEG, GIF)
  - Maximum file size: 5MB
  - Will be optimized and resized if necessary
- **Response**:
  ```json
  {
    "message": "Profile image updated successfully",
    "profile_image": "string (URL)"
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
- **Validation Rules**:
  - Email and password are required
  - Both must be strings
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
- **Validation Rules**:
  - Title:
    - Required
    - String
    - Maximum 200 characters
  - Description:
    - Required
    - String
  - Instructions:
    - Required
    - String
  - Category ID:
    - Required
    - Integer
  - Prep Time:
    - Optional
    - Non-negative integer
  - Cook Time:
    - Optional
    - Non-negative integer
  - Servings:
    - Optional
    - Positive integer
  - Ingredients:
    - Must be a list of objects
    - Each ingredient must have:
      - ingredient_id (integer)
      - quantity (positive number)
      - unit (string)
  - Dietary Restrictions:
    - Must be a list of integers
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
- **Validation Rules**:
  - Content:
    - Required
    - Must be a string
    - Cannot be empty
    - Maximum 1000 characters
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
- **Validation Rules**:
  - Rating:
    - Required
    - Must be an integer
    - Must be between 1 and 5
  - Only one rating per user per recipe (subsequent ratings update the existing one)
- **Response**:
  ```json
  {
    "message": "Rating submitted successfully"
  }
  ```
  or
  ```json
  {
    "message": "Rating updated successfully"
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
- **Validation Rules**:
  - Recipe must exist
  - Cannot favorite the same recipe twice
- **Response**:
  ```json
  {
    "message": "Recipe favorited successfully"
  }
  ```

#### Remove from Favorites
- **URL**: `/api/recipes/<recipe_id>/favorites`
- **Method**: `DELETE`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "message": "Recipe removed from favorites"
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
  "error": "Error message describing the issue",
  "details": [
    "List of specific validation errors (when applicable)"
  ]
}
```

Common HTTP status codes:
- **400 Bad Request**: Invalid input data or validation failure
  - Missing required fields
  - Invalid data types
  - Value out of allowed range
  - Duplicate entries (e.g., already favorited)
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
  - Recipe not found
  - Comment not found
  - Favorite not found

## Validation Rules Summary

### User Data
- Username: 3-50 characters, alphanumeric with underscores
- Email: Valid email format
- Password: 8+ characters, must include uppercase, lowercase, and number
- Profile Image: Valid HTTP(S) URL

### Recipe Data
- Title: Max 200 characters
- Numeric fields (prep_time, cook_time, servings): Non-negative integers
- Ingredients: Must include valid ingredient_id, positive quantity, and unit
- Dietary Restrictions: List of valid restriction IDs

### Comment Data
- Content: Required, non-empty string, max 1000 characters

### Rating Data
- Rating: Integer between 1 and 5
- One rating per user per recipe

### Favorite Data
- One favorite per user per recipe
- Recipe must exist to be favorited

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

## File Upload Configuration

The application supports two methods for storing uploaded files:

### Local Storage (Development)
- Files are stored in the `uploads` directory
- Served via `/uploads/<filename>` endpoint
- Configure via environment variable: `USE_S3=false`

### Amazon S3 Storage (Production)
- Files are stored in an S3 bucket
- Requires the following environment variables:
  - `USE_S3=true`
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION` (defaults to us-east-1)
  - `AWS_S3_BUCKET`

## Image Processing
- Supported formats: PNG, JPG, JPEG, GIF
- Maximum file size: 5MB
- Images are automatically:
  - Converted to JPEG format
  - Resized if larger than 800x800 pixels
  - Optimized for web delivery
  - Quality set to 85% 