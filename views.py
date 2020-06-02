import random
from functools import wraps

from flask import abort, flash, session, redirect, request, render_template, url_for


from app import app, db, IngredientGroups, Ingredients, Recipes
from forms import UserForm, RecipeForm
from models import User, IngredientGroup, Ingredient, Recipe, users_recipes, ingredients_recipes


@app.route('/')
def home_page():
    session_data = session.get('user', None)
    favor = None
    if session_data:
        favor = len(db.session.query(Recipe).filter(Recipe.list_users.any(User.user_id == session_data['user_id'])).all())

    print('from session_data {}'.format(session_data))
    #u_name = session.get('user_name', None)
#        return redirect(url_for('render_login'))
    list_recipes = db.session.query(Recipe).all()
    list_recipes = random.sample(list_recipes, k=6)
    print(list_recipes)
    #list_recipes = random.sample(Recipes, k=6)
    return render_template('index.html', about_user=session_data, fav=favor, list_recipes=list_recipes)


@app.route('/recipe/<int:recipe_id>/')
def render_recipe(recipe_id):
    session_data = session.get('user', None)
    favor = None
    btn_favor = True
    if session_data:
        favor = len(db.session.query(Recipe).filter(Recipe.list_users.any(User.user_id == session_data['user_id'])).all())
        list_favor = db.session.query(Recipe).filter(Recipe.list_users.any(User.user_id == session_data['user_id'])).all()
        for elem in list_favor:
            if elem.recipe_id == recipe_id:
                btn_favor = False
                break

    print('from session_data {}'.format(session_data))
    one_recipe = db.session.query(Recipe).get(recipe_id)
    list_ingredients = db.session.query(Ingredient).filter(Ingredient.in_recipes.any(Recipe.recipe_id == recipe_id)).all()

    print(list_ingredients)

    # for recipe in Recipes:
    #     if recipe['id'] == recipe_id:
    #         one_recipe = {key: val for key, val in recipe.items()}
    # print(one_recipe)
    # list_ingredients = []
    # for elem in Ingredients:
    #     if elem['id'] in one_recipe['ingredients']:
    #         list_ingredients.append(elem['title'])
    # print(list_ingredients)
    session_food = session.get('food')
    print('from session_food {}'.format(session_food))
    return render_template('recipe.html', about_user=session_data, fav=favor, btn_favor=btn_favor, recipe=one_recipe, ingredients=list_ingredients, session_food=session_food)


@app.route('/favorites/<int:recipe_id>/<action>/', methods=['GET', 'POST'])
def render_favorites(recipe_id, action):
    add_recipe = None
    session_data = session.get('user', None)
    if not session.get('user'):
        return redirect(url_for('render_login'))

    user = db.session.query(User).get(session_data['user_id'])
    if recipe_id != 0:
        one_recipe = db.session.query(Recipe).get(recipe_id)
        one_recipe.list_users.append(user)
        db.session.commit()

    if request.method == 'POST':
        print('удаление рецепта из избранного')
    list_recipes = db.session.query(Recipe).filter(Recipe.list_users.any(User.user_id == session_data['user_id'])).all()
    favor = len(list_recipes)
    #list_recipes = random.sample(Recipes, k=6)
    return render_template('fav.html', about_user=session_data, fav=favor, add_recipe=add_recipe, list_recipes=list_recipes)


@app.route('/wizard/')
def render_wizard():
    session_data = session.get('user', None)
    favor = None
    if session_data:
        favor = len(db.session.query(Recipe).filter(Recipe.list_users.any(User.user_id == session_data['user_id'])).all())

    full_groups = db.session.query(IngredientGroup).all()
    full_ingredients = db.session.query(Ingredient).all()

    list_group = []
    for elem in full_groups:
        list_group.append(elem.group_name)

    all_ingredients = []
    for elem in full_ingredients:
        tmp_dict = {}
        tmp_dict['part_id'] = elem.part_id
        tmp_dict['title'] = elem.ingredient_name
        tmp_dict['group_id'] = elem.id_group
        gr_name = db.session.query(IngredientGroup).get(elem.id_group)
        tmp_dict['group'] = gr_name.group_name
        all_ingredients.append(tmp_dict)


        # tmp_dict['group_id'] = elem['ingredient_group']
        # for gr in IngredientGroups:
        #     if tmp_dict['group_id'] == gr['id']:
        #         tmp_dict['group'] = gr['title']
        # all_ingredients.append(tmp_dict)
    for elem in full_ingredients:
        print(elem.part_id, elem.group)



    # list_group = []
    # for elem in IngredientGroups:
    #     list_group.append(elem['title'])
    # all_ingredients = []
    # for elem in Ingredients:
    #     tmp_dict = {}
    #     tmp_dict['id'] = elem['id']
    #     tmp_dict['title'] = elem['title']
    #     tmp_dict['group_id'] = elem['ingredient_group']
    #     for gr in IngredientGroups:
    #         if tmp_dict['group_id'] == gr['id']:
    #             tmp_dict['group'] = gr['title']
    #     all_ingredients.append(tmp_dict)

    #select_ingredts = [(el['id'], el['title']) for el in all_ingredients]
    #print(all_ingredients)
    #print(select_ingredts)
    session_food = session.get('food')
    # tmp = []
    # for el in session_food:
    #     tmp.append(int(el))
    # session_food = tmp
    print('from session food {}'.format(session_food))
    return render_template('list.html', about_user=session_data, fav=favor, groups=list_group, all_ingredients=all_ingredients, session_food=session_food)


@app.route('/wizard-results/', methods=['GET', 'POST'])
def render_wizard_results():
    session_data = session.get('user', None)
    favor = None
    if session_data:
        favor = len(db.session.query(Recipe).filter(Recipe.list_users.any(User.user_id == session_data['user_id'])).all())

    session['food'] = [int(x) for x in request.form.getlist("ingredients")]
    print('from wizard {}'.format(session['food']))

    list_recipes = []
    for elem in session['food']:
        one_recipes = db.session.query(Recipe).filter(Recipe.list_ingredients.any(Ingredient.part_id == int(elem))).all()
        list_recipes.append(one_recipes)
#    print(one_recipes[0].recipe_id)

    # list_recipes = []
    # for recipe in Recipes:
    #     for elem in session['food']:
    #         if int(elem) in recipe['ingredients']:
    #             list_recipes.append(recipe)
    print(len(list_recipes))
    print(list_recipes)

    return render_template('recipes.html', about_user=session_data, fav=favor, list_recipes=list_recipes)


@app.route('/register', methods=['GET', 'POST'])
def render_register():
    session_data = session.get('user', None)
    form = UserForm()
    error_msg = ''
    if request.method == 'POST':
        u_name = form.usr_name.data
        u_email = form.usr_email.data
        #u_password = form.usr_password.data


        form.validate_on_submit()
        if form.usr_name.errors or form.usr_email.errors or form.usr_password.errors:
            error_msg = 'Неверно указано имя, email или пароль'
            print(error_msg)
            return render_template('registr.html', about_user=session_data, form=form, error_msg=error_msg)

        # проверка наличия пользователя в БД
        user = db.session.query(User).filter(User.email == u_email).first()
        # Если такой пользователь существует
        if user:
            # Не можем зарегистрировать, так как пользователь уже существует
            error_msg = 'Пользователь с указанным email уже существует'
            return render_template('login.html', about_user=session_data, form=form, error_msg=error_msg)

        # сохранение данных о пользователе в БД, session и переходим на Home_page
        user = User(user_name=u_name, email=u_email, is_admin=False)
        user.password = form.usr_password.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('home_page'))

    return render_template('registr.html', about_user=session_data, form=form, error_msg=error_msg)


@app.route('/login', methods=['GET', 'POST'])
def render_login():
    session_data = session.get('user', None)
    form = UserForm()
    error_msg = ''
    if request.method == 'POST':
        u_email = form.usr_email.data
        #u_password = form.usr_password.data

        form.validate_on_submit()
        if form.usr_email.errors or form.usr_password.errors:
            error_msg = 'Неверно указан email или пароль'
            print(error_msg)
            print(form.usr_email.errors, form.usr_password.errors)
            return render_template('login.html', about_user=session_data, form=form, error_msg=error_msg)

        # проверка наличия пользователя в БД
        user = db.session.query(User).filter(User.email == u_email).first()
        # Если такой пользователь не существует
        if not user:
            error_msg = 'Пользователь с указанным email не существует. Пройдите регистрацию.'
            return render_template('registr.html', about_user=session_data, form=form, error_msg=error_msg)

        # Если такой пользователь существует, но пароль неверен
        if not user.password_valid(form.usr_password.data):
            error_msg = 'Для пользователя указан неверный пароль'
            return render_template('login.html', about_user=session_data, form=form, error_msg=error_msg)

        # сохранение данных о пользователе в session и переходим на Home_page
        session['user'] = {
            'user_id': user.user_id,
            'username': user.user_name,
            'email': user.email,
            'admin': user.is_admin,
        }
        session_data = session.get('user', None)
        #return "Вы зашли успешно"
        #error_msg = 'Вы зашли успешно'
        #return render_template('login.html', form=form, error_msg=error_msg)
        return redirect(url_for('home_page'))

    return render_template('login.html', about_user=session_data, form=form, error_msg=error_msg)


@app.route('/new_recipe/', methods=['GET', 'POST'])
def render_new_recipe():
    session_data = session.get('user', None)
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

    return render_template('new_recipe.html', about_user=session_data, form=form)


@app.route('/logout', methods=['GET', 'POST'])
def render_logout():
    if session.get('user'):
        session.clear()


    #return redirect(url_for('home_page'))
    return redirect(url_for('render_login'))


@app.route('/about/')
def render_about():
    """
    Представление страницы "О сервисе"
    :return: Описание сервиса
    """
    session_data = session.get('user', None)
    return render_template('about.html', about_user=session_data)