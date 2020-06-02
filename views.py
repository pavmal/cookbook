from flask import session, redirect, request, render_template, url_for

from app import app, db
from forms import UserForm, RecipeForm
from models import User, IngredientGroup, Ingredient, Recipe, users_recipes, ingredients_recipes


@app.route('/')
def home_page():
    """
    Главная (домашняя) страница. Выводит список 6 рецептов и проверяет наличие авторизованного пользователя
    :return: 6 рецептов из базы. Пока не формирует список наиболее популярных (добавленных в избранное)
    """
    session_data = session.get('user', None)  # проверка прежнего использования сайта через session
    favor = None  # для отражения данных о наличии избранных рецептов у авторизованных пользователей
    if session_data:
        favor = len(
            db.session.query(Recipe).filter(Recipe.list_users.any(User.user_id == session_data['user_id'])).all())

    list_recipes = db.session.query(Recipe).order_by(db.func.random()).limit(6)

    return render_template('index.html', about_user=session_data, fav=favor, list_recipes=list_recipes)


@app.route('/recipe/<int:recipe_id>/')
def render_recipe(recipe_id):
    """
    Форма отражения сведений о рецепте
    :param recipe_id: id рецепта
    :return: Информация о рецепте
    """
    session_data = session.get('user', None)
    favor = None
    btn_favor = False  # для достпности кнопки на форме "Добавить в избранное"
    if session_data:
        favor = len(
            db.session.query(Recipe).filter(Recipe.list_users.any(User.user_id == session_data['user_id'])).all())
        list_favor = db.session.query(Recipe).filter(
            Recipe.list_users.any(User.user_id == session_data['user_id'])).all()
        btn_favor = True
        for elem in list_favor:
            if elem.recipe_id == recipe_id:
                btn_favor = False
                break
    one_recipe = db.session.query(Recipe).get(recipe_id)
    list_ingredients = db.session.query(Ingredient).filter(
        Ingredient.in_recipes.any(Recipe.recipe_id == recipe_id)).all()

    session_food = session.get('food')  # проверка наличия ранее выбранных продуктов в холодильнике

    return render_template('recipe.html', about_user=session_data, fav=favor, btn_favor=btn_favor, recipe=one_recipe,
                           ingredients=list_ingredients, session_food=session_food)


@app.route('/favorites/<int:recipe_id>/<action>/', methods=['GET', 'POST'])
def render_favorites(recipe_id, action):
    """
    Фома отражения списка рецептов из Избранного
    :param recipe_id: id рецепа для добавления в Избранное
    :param action: 0: просмотр списка, 1: добавление рецепта в Избранное, -1: удаление из Избранного
    :return:
    """
    add_recipe = action
    session_data = session.get('user', None)
    if not session.get('user'):  # если пользователь не авторизован, то нельзя добавить рецепт в Избранное
        return redirect(url_for('render_login'))

    user = db.session.query(User).get(session_data['user_id'])
    if recipe_id > 0:  # добавление в Избранное
        one_recipe = db.session.query(Recipe).get(recipe_id)
        one_recipe.list_users.append(user)
        db.session.commit()

    if request.method == 'POST':  # удаление из Избранного
        one_recipe = db.session.query(Recipe).get(recipe_id)
        one_recipe.list_users.remove(user)
        db.session.commit()

    list_recipes = db.session.query(Recipe).filter(Recipe.list_users.any(User.user_id == session_data['user_id'])).all()
    favor = len(list_recipes)

    return render_template('fav.html', about_user=session_data, fav=favor, add_recipe=add_recipe,
                           list_recipes=list_recipes)


@app.route('/wizard/')
def render_wizard():
    """
    Форма выбора продуктов, которые есть у пользователя
    :return: Список рецептов, в которых встречается хоть один ингредиент из выбранного списка
    """
    session_data = session.get('user', None)
    favor = None
    if session_data:
        favor = len(
            db.session.query(Recipe).filter(Recipe.list_users.any(User.user_id == session_data['user_id'])).all())

    full_groups = db.session.query(IngredientGroup).all()
    full_ingredients = db.session.query(Ingredient).all()

    list_group = []  # список групп продуктов для вывода продуктов с группировкой
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

    session_food = session.get('food')  # проверка наличия ранее выбранных продуктов в холодильнике

    return render_template('list.html', about_user=session_data, fav=favor, groups=list_group,
                           all_ingredients=all_ingredients, session_food=session_food)


@app.route('/wizard-results/', methods=['GET', 'POST'])
def render_wizard_results():
    """
    Форма вывода результатов поиска рецептов
    :return: Список рецептов, в которых есть хоть 1 ингредиент, который есть у пользователя в холодильнике
    """
    session_data = session.get('user',
                               None)  # для отражения количества Избранных рецептов у авторизованных пользователей
    favor = None
    if session_data:
        favor = len(
            db.session.query(Recipe).filter(Recipe.list_users.any(User.user_id == session_data['user_id'])).all())

    # преобразование элементов списка из строк в цифры
    session['food'] = [int(x) for x in request.form.getlist("ingredients")]

    list_recipes = []
    for elem in session['food']:
        one_recipes = db.session.query(Recipe).filter(
            Recipe.list_ingredients.any(Ingredient.part_id == int(elem))).all()
        list_recipes.append(one_recipes)

    return render_template('recipes.html', about_user=session_data, fav=favor, list_recipes=list_recipes)


@app.route('/register', methods=['GET', 'POST'])
def render_register():
    """
    Форма для регистрации новых пользователей
    :return: Новый пользователь в базе
    """
    session_data = session.get('user', None)
    form = UserForm()
    error_msg = ''
    if request.method == 'POST':
        u_name = form.usr_name.data
        u_email = form.usr_email.data

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
        session['user'] = {
            'user_id': user.user_id,
            'username': user.user_name,
            'email': user.email,
            'admin': user.is_admin,
        }

        return redirect(url_for('home_page'))

    return render_template('registr.html', about_user=session_data, form=form, error_msg=error_msg)


@app.route('/login', methods=['GET', 'POST'])
def render_login():
    """
    Форма авторизации пользователей
    :return: Авторизованный пользователь с отображением Избранного
    """
    session_data = session.get('user', None)
    form = UserForm()
    error_msg = ''
    if request.method == 'POST':
        u_email = form.usr_email.data

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
        return redirect(url_for('home_page'))

    return render_template('login.html', about_user=session_data, form=form, error_msg=error_msg)


@app.route('/new_recipe/', methods=['GET', 'POST'])
def render_new_recipe():
    """
    Форма для ввода новых рецептов
    :return: Добавление рецепта в базу. Пока нет возможности указать продукты
    """
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
    """
    Форма для выхода
    :return: Неавторизованный пользователь. Очиста сессии
    """
    if session.get('user'):
        session.clear()
    # return redirect(url_for('home_page'))
    return redirect(url_for('render_login'))


@app.route('/about/')
def render_about():
    """
    Представление страницы "О сервисе"
    :return: Описание сервиса
    """
    session_data = session.get('user', None)
    return render_template('about.html', about_user=session_data)
