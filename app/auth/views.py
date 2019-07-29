from flask import render_template
from . import auth

@auth.routh('/login')
def login():
    return render_template('auth/login.html')
