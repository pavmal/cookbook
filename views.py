from functools import wraps

from flask import abort, flash, session, redirect, request, render_template, url_for


from app import app, db
#from models import User
#from forms import LoginForm, RegistrationForm, ChangePasswordForm

@app.route('/')
def index():
    return render_template('index.html')
