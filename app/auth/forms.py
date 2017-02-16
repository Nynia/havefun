from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField

class LoginForm(Form):
    phonenum = StringField('username')
    password = PasswordField('password')
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')