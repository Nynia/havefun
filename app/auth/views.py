# -*-coding:utf-8-*-
from . import auth
from flask_login import login_user, logout_user, login_required,current_user
from flask import render_template, redirect, request, url_for, flash, session, request, jsonify
from ..models import User, OrderRelation
from .forms import LoginForm, RegisterFrom
from ..utils.func import generate_identifying_code

cache = {}
from app import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(phonenum=form.phonenum.data).first()
            if user is not None and user.verify_password(form.password.data):
                login_user(user, True)

                relation = OrderRelation.query.filter_by(phonenum=user.phonenum).all()
                for r in relation:
                    if r.status == '1':
                        session[r.productid] = 1
                session['phonenum'] = user.phonenum
                next = request.args.get('next')
                print session.get('user_id')
                return redirect(next or url_for('main.my'))
            flash(u'用户名或密码错误', 'login')
        else:
            flash(u'请输入正确的手机号码', 'login')
    return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    if 'phonenum' in session:
        phonenum = session.pop('phonenum')
        relation = OrderRelation.query.filter_by(phonenum=phonenum).all()
        for r in relation:
            if r.productid in session:
                session.pop(r.productid)
    return 'logout success'


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterFrom()
    action = request.args.get('action')
    if action == 'getIdentifingCode':
        phonenum = request.args.get('phonenum')
        print phonenum
        code = generate_identifying_code()
        msg = u'【玩乐派】尊敬的用户：您的校验码为%s，有效时间2分钟，感谢使用' % code
        cache[phonenum] = code
        print cache
        import requests
        url = 'http://221.228.17.88:8080/sendmsg/send'
        params = {
            'phonenum': phonenum,
            'msg': msg
        }
        r = requests.get(url, params=params)
        print r.text
        return jsonify({
            'phonenum': phonenum,
            'msg': msg
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
            else:
                flash(u'用户已存在，不能重复注册', 'register')
        else:
            flash(u'验证码输入错误', 'register')
    return render_template('register.html', form=form)


@auth.before_app_request
def before_request():
    if session.get('user_id') and not session.get('phonenum'):
        user = User.query.get(int(session.get('user_id')))
        if user:
            print user.phonenum
            login_user(user, True)
            relation = OrderRelation.query.filter_by(phonenum=user.phonenum).all()
            for r in relation:
                if r.status == '1':
                    session[r.productid] = 1
            session['phonenum'] = user.phonenum
    #else:
    #   session['user_id'] = current_user.id
