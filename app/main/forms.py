from flask.ext.wtf import Form
from wtforms import StringField,IntegerField,TextAreaField,FileField,SubmitField

class GameForm(Form):
    name = StringField('name')
    packageid = IntegerField('packageid')
    brief = TextAreaField('brief')
    type = StringField('tpye')
    category = StringField('category')
    star = IntegerField('star')
    size = StringField('size(M)')
    apk = FileField('apk')
    icon = FileField('icon')
    screenshot = FileField('screenshot')
    submit = SubmitField('submit')

