import random
from functools import wraps

from flask import abort, flash, session, redirect, request, render_template, url_for


from app import app, db, IngredientGroups, Ingredients, Recipes
from forms import UserForm, IngredientForm, RecipeForm
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
    list_group = []
    for elem in IngredientGroups:
        list_group.append(elem['title'])
    all_ingredients = []
    for elem in Ingredients:
        tmp_dict = {}
        tmp_dict['id'] = elem['id']
        tmp_dict['title'] = elem['title']
        tmp_dict['group_id'] = elem['ingredient_group']
        for gr in IngredientGroups:
            if tmp_dict['group_id'] == gr['id']:
                tmp_dict['group'] = gr['title']
        all_ingredients.append(tmp_dict)

    select_ingredts = [(el['id'], el['title']) for el in all_ingredients]
    print(all_ingredients)
    print(select_ingredts)
    form = IngredientForm()
    form.ingredients.choices = select_ingredts
    return render_template('list.html', groups=list_group, all_ingredients=all_ingredients, form=form)


@app.route('/wizard-results/', methods=['GET', 'POST'])
def render_wizard_results():

    selected = request.form.getlist("ingredients")
    print(selected)
    return render_template('recipes.html')


@app.route('/register', methods=['GET', 'POST'])
def render_register():

    form = UserForm()
    error_msg = ''
    if request.method == 'POST':
        user_name = form.usr_name.data
        user_email = form.usr_email.data
        user_password = form.usr_password.data

        form.validate_on_submit()
        if form.usr_name.errors or form.usr_email.errors or form.usr_password.errors:
            error_msg = "Неверно указано имя, email или пароль"
            print(error_msg)
            return render_template("registr.html", form=form, error_msg=error_msg)

        # # проверка наличия пользователя в БД
        # user = db.session.query(User).filter(User.email == user_email).first()
        # # Если такой пользователь существует
        # if user:
        #     # Не можем зарегистрировать, так как пользователь уже существует
        #     error_msg = "Пользователь с указанным email уже существует"
        #     return render_template("login.html", error_msg=error_msg)

        # сохранение данных о пользователе в БД, session и переходим на Home_page
        return redirect(url_for('home_page'))

    return render_template('registr.html', form=form, error_msg=error_msg)


@app.route('/login', methods=['GET', 'POST'])
def render_login():
    form = UserForm()
    error_msg = ''
    if request.method == 'POST':
        user_email = form.usr_email.data
        user_password = form.usr_password.data

        form.validate_on_submit()
        if form.usr_email.errors or form.usr_password.errors:
            error_msg = 'Неверно указан email или пароль'
            print(error_msg)
            print(form.usr_email.errors, form.usr_password.errors)
            return render_template('login.html', form=form, error_msg=error_msg)

        # # проверка наличия пользователя в БД
        # user = db.session.query(User).filter(User.email == user_email).first()
        # # Если такой пользователь не существует
        # if not user:
        #     error_msg = "Пользователь с указанным email не существует. Пройдите регистрацию."
        #     return render_template('registr.html', form=form, error_msg=error_msg)

        # # Если такой пользователь существует, но пароль неверен
        # if user and пароль неверен:
        #     error_msg = "Для пользователя указан неверный пароль"
        #     return render_template('login.html', form=form, error_msg=error_msg)

        # сохранение данных о пользователе в session и переходим на Home_page
        # session['user_id'] = user_id
        #session['user_name'] = user_name
        #session['user_email'] = user_email
        #return "Вы зашли успешно"
        #error_msg = 'Вы зашли успешно'
        #return render_template('login.html', form=form, error_msg=error_msg)
        return redirect(url_for('home_page'))

    return render_template('login.html', form=form, error_msg=error_msg)


@app.route('/new_recipe/', methods=['GET', 'POST'])
def render_new_recipe():
    form = RecipeForm()
    error_msg = ''
    if request.method == 'POST':
        pass
        r_name = form.recipe_name.data
        r_picture = form.picture.data
        r_description = form.description.data
        r_time = form.time.data
        r_servings = form.servings.data
        r_kcal = form.kcal.data
        r_instruction = form.instruction.data

    return render_template('new_recipe.html', form=form)


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