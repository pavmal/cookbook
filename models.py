from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

# Настройки соединения сделаем позже в модуле приложения
# db = SQLAlchemy()

# ---------------------------------------------------------
# database Models

users_recipes = db.Table('users_recipes',
                         db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
                         db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.recipe_id'))
                         )

ingredients_recipes = db.Table('ingredients_recipes',
                               db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.ingredient_id')),
                               db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.recipe_id'))
                               )


class IngredientGroup(db.Model):
    __tablename__ = 'ingredient_groups'
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(150), unique=True, nullable=False)
    ingredient = db.relationship('Ingredient', back_populates='group')
#
#
class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    ingredient_id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, nullable=False)  # id Ingredients
    ingredient_name = db.Column(db.String(200), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('ingredient_groups.group_id'))
    group = db.relationship('IngredientGroup', back_populates='ingredient')
    in_recipes = db.relationship('Recipe', secondary=ingredients_recipes, back_populates='list_ingredients')


class Recipe(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(150), unique=True, nullable=False)
    picture = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    kcal = db.Column(db.Float, nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    list_ingredients = db.relationship('Ingredient', secondary=ingredients_recipes, back_populates='in_recipes')
    list_users = db.relationship('User', secondary=users_recipes, back_populates='favorite_recipes')


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    favorite_recipes = db.relationship('Recipe', secondary=users_recipes, back_populates='list_users')

    @property
    def password(self):
        # Запретим прямое обращение к паролю
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        # Устанавливаем пароль через этот метод
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        # Проверяем пароль через этот метод
        # Функция check_password_hash превращает password в хеш и сравнивает с хранимым
        return check_password_hash(self.password_hash, password)



db.create_all()
