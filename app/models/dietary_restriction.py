from app import db

class DietaryRestriction(db.Model):
    __tablename__ = 'dietary_restrictions'
    dietary_restriction_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class RecipeDietaryRestriction(db.Model):
    __tablename__ = 'recipe_dietary_restrictions'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id', ondelete='CASCADE'), nullable=False)
    dietary_restriction_id = db.Column(db.Integer, db.ForeignKey('dietary_restrictions.dietary_restriction_id', ondelete='CASCADE'), nullable=False) 