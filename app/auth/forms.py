#-*-coding:utf-8-*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import Regexp,DataRequired
class LoginForm(FlaskForm):
    phonenum = StringField(validators=[Regexp('^1[3|5|7|8][0-9]{9}$',0,'phone error')])
    password = PasswordField()
    submit = SubmitField()

class RegisterFrom(FlaskForm):
    phonenum = StringField(validators=[Regexp('^1[3|5|7|8][0-9]{9}$', 0, 'phone error')])
    password = PasswordField()
    vercode = IntegerField(validators=[DataRequired()])
    submit = SubmitField()