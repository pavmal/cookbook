import random
from functools import wraps

from flask import abort, flash, session, redirect, request, render_template, url_for


from app import app, db, IngredientGroups, Ingredients, Recipes
#from models import User
#from forms import LoginForm, RegistrationForm, ChangePasswordForm

@app.route('/')
def home_page():
    list_recipes = random.sample(Recipes, k=6)
    return render_template('index.html', list_recipes=list_recipes)


@app.route('/recipe/<int:recipe_id>/')
def render_recipe(recipe_id):
    for recipe in Recipes:
        if recipe['id'] == recipe_id:
            one_recipe = {key: val for key, val in recipe.items()}
    print(one_recipe)
    list_ingredients = []
    for elem in Ingredients:
        if elem['id'] in one_recipe['ingredients']:
            list_ingredients.append(elem['title'])
    print(list_ingredients)
    return render_template('recipe.html', recipe=one_recipe, ingredients=list_ingredients)



@app.route('/about/')
def render_about():
    """
    Представление страницы "О сервисе"
    :return: Описание сервиса
    """
    return render_template('about.html')