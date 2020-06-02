import os, json, random, re

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_debugtoolbar import DebugToolbarExtension
from config import Config
#from models import
from data import IngredientGroups, Ingredients, Recipes
#from models import User, IngredientGroup, Ingredient, Recipe, users_recipes, ingredients_recipes

NEED_IMPORT = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
#db.init_app(app)


# Имортируем представление
from views import *

migrate = Migrate(app, db)



if __name__ == '__main__':

    if NEED_IMPORT:
        for elem in IngredientGroups:
            ingred_gr = IngredientGroup(group_name=elem['title'])
            db.session.add(ingred_gr)
            print('загрузка {}'.format(elem['title']))
        db.session.commit()

        for elem in Ingredients:
            group_ingrd = db.session.query(IngredientGroup).get(elem['ingredient_group'])
            one_ingredient = Ingredient(part_id=elem['id'], ingredient_name=elem['title'], active=True, group=group_ingrd)
            db.session.add(one_ingredient)
            print('загрузка {} группа {}'.format(elem['title'], group_ingrd.group_name))
        db.session.commit()

        for elem in Recipes:
            one_recipe = Recipe(recipe_name=elem['title'], picture=elem['picture'], description=elem['description'], time=elem['time'],
                                servings=elem['servings'], kcal=elem['kcal'], instruction=elem['instruction'], is_active=True)
            db.session.add(one_recipe)
            for i in elem['ingredients']:
                part_num = db.session.query(Ingredient).filter(Ingredient.part_id == i).first()
                one_recipe.list_ingredients.append(part_num)
        db.session.commit()

    app.run('127.0.0.1', 5050, debug=True)
    #app.run()  # for gunicorn server
toolbar = DebugToolbarExtension(app)