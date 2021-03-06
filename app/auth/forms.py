#-*-coding:utf-8-*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Regexp,DataRequired

class LoginForm(FlaskForm):
    phonenum = StringField(validators=[Regexp('^1[3|5|7|8][0-9]{9}$',0,'phone error')])
    password = PasswordField()
    submit = SubmitField()

class RegisterFrom(FlaskForm):
    phonenum = StringField(validators=[Regexp('^1[3|5|7|8][0-9]{9}$', 0, 'phone error')])
    password = PasswordField()
    vercode = StringField(validators=[DataRequired()])
    submit = SubmitField()

class ResetForm(FlaskForm):
    phonenum = StringField(validators=[Regexp('^1[3|5|7|8][0-9]{9}$', 0, 'phone error')])
    vercode = StringField(validators=[DataRequired()])
    submit = SubmitField()

class ResetSubmitForm(FlaskForm):
    phonenum = StringField()
    password = PasswordField()
    submit = SubmitField()