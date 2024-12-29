-- Create Users Table
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    profile_image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Categories Table
CREATE TABLE Categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create Recipes Table
CREATE TABLE Recipes (
    recipe_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    instructions TEXT NOT NULL,
    category_id INT NOT NULL,
    image_url TEXT,
    prep_time INT,
    cook_time INT,
    servings INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES Categories (category_id) ON DELETE SET NULL
);

-- Create Ingredients Table
CREATE TABLE Ingredients (
    ingredient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create Recipe_Ingredients Table
CREATE TABLE Recipe_Ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    quantity NUMERIC(10, 2) NOT NULL,
    unit VARCHAR(50) NOT NULL,
    CONSTRAINT fk_recipe FOREIGN KEY (recipe_id) REFERENCES Recipes (recipe_id) ON DELETE CASCADE,
    CONSTRAINT fk_ingredient FOREIGN KEY (ingredient_id) REFERENCES Ingredients (ingredient_id) ON DELETE CASCADE
);

-- Create Ratings Table
CREATE TABLE Ratings (
    rating_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_rating FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_recipe_rating FOREIGN KEY (recipe_id) REFERENCES Recipes (recipe_id) ON DELETE CASCADE
);

-- Create Comments Table
CREATE TABLE Comments (
    comment_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_comment FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_recipe_comment FOREIGN KEY (recipe_id) REFERENCES Recipes (recipe_id) ON DELETE CASCADE
);

-- Create Favorites Table
CREATE TABLE Favorites (
    favorite_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_favorite FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_recipe_favorite FOREIGN KEY (recipe_id) REFERENCES Recipes (recipe_id) ON DELETE CASCADE
);

-- Create Dietary_Restrictions Table
CREATE TABLE Dietary_Restrictions (
    dietary_restriction_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Create Recipe_Dietary_Restrictions Table (Many-to-Many)
CREATE TABLE Recipe_Dietary_Restrictions (
    id SERIAL PRIMARY KEY,
    recipe_id INT NOT NULL,
    dietary_restriction_id INT NOT NULL,
    CONSTRAINT fk_recipe_dietary FOREIGN KEY (recipe_id) REFERENCES Recipes (recipe_id) ON DELETE CASCADE,
    CONSTRAINT fk_dietary FOREIGN KEY (dietary_restriction_id) REFERENCES Dietary_Restrictions (dietary_restriction_id) ON DELETE CASCADE
);

-- Insert Initial Data for Categories (Optional)
INSERT INTO Categories (name)
VALUES 
('Appetizers'),
('Main Courses'),
('Desserts'),
('Beverages');

-- Insert Initial Data for Dietary Restrictions (Optional)
INSERT INTO Dietary_Restrictions (name)
VALUES 
('Vegetarian'),
('Vegan'),
('Gluten-Free'),
('Nut-Free'),
('Dairy-Free'),
('Halal'),
('Kosher');
