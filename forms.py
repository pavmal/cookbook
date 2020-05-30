import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, HiddenField, SelectField, TextAreaField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, InputRequired, Email

from app import app, db, IngredientGroups, Ingredients, Recipes


class UserForm(FlaskForm):
    """
    usr_email: поле для ввода email
    usr_password: поле для ввода пароля пользователя
    usr_admin: невидимое поле, устанавливает по умолчанию, что пользователи - не админы
    submit: кнопка отправки формы на обработку
    """
    usr_name = StringField('Ваше имя', validators=[Length(min=1), InputRequired()])
    usr_email = StringField('Ваш email', validators=[Email(), Length(min=3), InputRequired()])
    usr_password = StringField('Ваш пароль (минимум 4 символа)', validators=[Length(min=4), InputRequired()])
    usr_admin = HiddenField('Администратор', default=False)
    submit = SubmitField('Запись данных')

class IngredientForm(FlaskForm):
    name = StringField('Название', validators=[InputRequired()])
    ingredients = SelectField('Состав блюда', coerce=int, validators=[InputRequired])


class RecipeForm(FlaskForm):
    recipe_name = StringField('Название рецепта', validators=[Length(min=3), InputRequired()])
    picture = StringField('Фото', validators=[Length(min=5), InputRequired()])
    description = TextAreaField('Краткое описаине')
    time = IntegerField('Время приготовления')
    servings = IntegerField('Количество порций')
    kcal = FloatField('Калорий в 1 порции')
    instruction = TextAreaField('Инструкция по приготовлению')
    list_ingredients = SelectField('Состав блюда', coerce=int, validators=[InputRequired])

