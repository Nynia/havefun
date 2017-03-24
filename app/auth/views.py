from . import auth
from flask_login import login_user, logout_user, login_required
from flask import render_template, redirect, request, url_for, flash, session, request, jsonify, g
from ..models import User, OrderRelation
from .forms import LoginForm, RegisterFrom
from ..utils.func import generate_identifying_code

cache = {}
from app import db


@auth.route('/login', methods=['GET', 'POST'])
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

@auth.route('/register', methods=['GET', 'POST'])
def register():
    print cache
    form = RegisterFrom()
    action = request.args.get('action')
    if action == 'getIdentifingCode':
        phonenum = request.args.get('phonenum')
        code = generate_identifying_code()
        cache[phonenum] = code

        import requests
        url = 'http://221.228.17.88:8080/sendmsg/send'
        params = {
            'phonenum': phonenum,
            'msg': code
        }
        r = requests.get(url, params=params)
        return jsonify({
            'phonenum': phonenum,
            'msg': code
        })
    if request.method == 'POST':
        phonenum = form.phonenum.data
        vercode = form.vercode.data
        password = form.password.data
        print cache
        if vercode == cache.get(phonenum):
            phonenum = request.form.get('phonenum')
            user = User.query.filter_by(phonenum=phonenum).first()
            from datetime import datetime
            if not user:
                user = User()
                user.phonenum = phonenum
                user.password = password
                user.integral = 0
                user.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
                db.session.add(user)
                db.session.commit()

                login_user(user, True)
                relation = OrderRelation.query.filter_by(phonenum=user.phonenum).all()
                orderedpro = []
                for r in relation:
                    if r.status == '1':
                        orderedpro.append(r.productid)
                session['ordered'] = orderedpro
                session['phonenum'] = user.phonenum
                print session
                next = request.args.get('next')
                return redirect(next or url_for('main.my'))
    return render_template('register.html', form=form)
