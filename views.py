import random
from functools import wraps

from flask import abort, flash, session, redirect, request, render_template, url_for


from app import app, db, IngredientGroups, Ingredients, Recipes
from forms import UserForm
from models import User #, RegistrationForm, ChangePasswordForm


@app.route('/')
def home_page():
    u_name = session.get('user_name', None)
#        return redirect(url_for('render_login'))
    list_recipes = random.sample(Recipes, k=6)
    return render_template('index.html', u_name=u_name, list_recipes=list_recipes)


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


@app.route('/favorites/')
def render_favorites():
    if not session.get('user_id'):
        return redirect(url_for('render_login'))

    list_recipes = random.sample(Recipes, k=6)
    return render_template('fav.html', list_recipes=list_recipes)


@app.route('/wizard/')
def render_wizard():
    return render_template('list.html')


@app.route('/wizard-results/')
def render_wizard_results():
    return render_template('recipes.html')


@app.route('/register', methods=['GET', 'POST'])
def render_register():

    form = UserForm()
    error_msg = ''
    if request.method == 'POST':
        user_name = form.usr_name.data
        user_email = form.usr_email.data
        user_password = form.usr_password.data

        if not form.validate_on_submit():
            error_msg = "Неверно указано имя, email или пароль"
            print(error_msg)
            return render_template("register.html", form=form, error_msg=error_msg)

        # # проверка наличия пользователя в БД
        # user = db.session.query(User).filter(User.email == user_email).first()
        # # Если такой пользователь существует
        # if user:
        #     # Не можем зарегистрировать, так как пользователь уже существует
        #     error_msg = "Пользователь с указанным email уже существует"
        #     return render_template("login.html", error_msg=error_msg)

        # сохранение данных о пользователе в БД

    return render_template('registr.html', form=form, error_msg=error_msg)


@app.route('/login', methods=['GET', 'POST'])
def render_login():
    form = UserForm()
    error_msg = ''
    if request.method == 'POST':
        user_name = form.usr_name.data
        user_email = form.usr_email.data
        user_password = form.usr_password.data

        if not form.validate_on_submit():
            error_msg = "Неверно указан email или пароль"
            print(error_msg)
            return render_template("login.html", form=form, error_msg=error_msg)

        session['user_name'] = user_name
        session['user_email'] = user_email
        return "Вы зашли успешно"


    return render_template('login.html', form=form, error_msg=error_msg)


@app.route('/logout', methods=['POST'])
def render_logout():
    if session.get('user_name'):
        session.pop('user_name')
        session.pop('user_email')
    return redirect(url_for('render_login'))


@app.route('/about/')
def render_about():
    """
    Представление страницы "О сервисе"
    :return: Описание сервиса
    """
    return render_template('about.html')