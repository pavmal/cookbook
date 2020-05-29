import os, json, random, re

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_debugtoolbar import DebugToolbarExtension
from config import Config
#from models import db
from data import IngredientGroups, Ingredients, Recipes

NEED_IMPORT = True


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
            pass
            print(elem['title'])

    app.run('127.0.0.1', 5050, debug=True)
    #app.run()  # for gunicorn server
toolbar = DebugToolbarExtension(app)