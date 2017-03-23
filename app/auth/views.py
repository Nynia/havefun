from . import auth
from flask_login import login_user, logout_user, login_required
from flask import render_template, redirect, request, url_for, flash,session,request
from ..models import User,OrderRelation
from .forms import LoginForm,RegisterFrom
from ..utils.func import generate_identifying_code
@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phonenum=form.phonenum.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            relation = OrderRelation.query.filter_by(phonenum=user.phonenum).all()
            orderedpro = []
            for r in relation:
                if r.status == '1':
                    orderedpro.append(r.productid)
            session['ordered'] = orderedpro
            session['phonenum'] = user.phonenum
            next = request.args.get('next')
            print session['user_id']
            return redirect(next or url_for('main.my'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return 'logout success'

@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterFrom()
    codemap = {}
    action = request.args.get('action')
    if action == 'getIdentifingCode':
        phonenum = request.args.get('phonenum')
        code = generate_identifying_code()
        codemap.__setattr__(phonenum,code)
        import requests
        url = 'http://221.228.17.88:8080/sendmsg/send'
        params = {
            'phonenum':phonenum,
            'msg':code
        }
        r = requests.get(url,params=params)
        print r.text
    if form.validate_on_submit():
        pass

    return render_template('register.html',form=form)