#-*-coding:utf-8-*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import Regexp,DataRequired

class LoginForm(Form):
    phonenum = StringField(validators=[Regexp('^1[3|5|7|8][0-9]{9}$',0,'phone error')])
    password = PasswordField()
    submit = SubmitField()

class RegisterFrom(Form):
    phonenum = StringField(validators=[Regexp('^1[3|5|7|8][0-9]{9}$', 0, 'phone error')])
    password = PasswordField()
    vercode = IntegerField(validators=[DataRequired()])
    submit = SubmitField()