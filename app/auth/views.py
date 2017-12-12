# -*-coding:utf-8-*-
from . import auth
from flask_login import login_user, logout_user, login_required,current_user
from flask import render_template, redirect, url_for, flash, session, request, jsonify
from ..models import User, OrderRelation, CheckinRecord,IntegralStrategy,IntegralRecord
from .forms import LoginForm, RegisterFrom,ResetForm
from ..utils.func import generate_identifying_code
import datetime
from ..utils.aes import aescrypt

cache = {}
from app import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    ua = request.user_agent.__str__()
    next = request.args.get('next')
    print ua
    if ua.find('appChannel') != -1:
        channel = ua[ua.find('appChannel')+11:-1]
    else:
        channel = None
    print channel

    if channel != None:
        print url_for('main.my')
        return render_template('freepasswd.html', nextUrl=next or url_for('main.my'))
    else:
        form = LoginForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                user = User.query.filter_by(phonenum=form.phonenum.data).first()
                #AES 解密
                password_decipher = aescrypt('1234567812345678').decrypt(form.password.data)
                if user is not None and user.verify_password(password_decipher):
                    login_user(user, True)
                    relation = OrderRelation.query.filter_by(phonenum=user.phonenum).all()
                    for r in relation:
                        if r.status == '1':
                            session[r.productid] = 1
                    session['phonenum'] = user.phonenum
                    #next = request.args.get('next')
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
        print password
        print cache
        if vercode == cache.get(phonenum):
            phonenum = request.form.get('phonenum')
            user = User.query.filter_by(phonenum=phonenum).first()
            from datetime import datetime
            if not user:
                user = User()
                user.phonenum = phonenum
                user.password = password
                integral_strategy = IntegralStrategy.query.filter_by(description=u'注册帐号').first()
                user.integral = integral_strategy.value
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


@auth.route('/checkin', methods=['GET'])
def checkin():
    uid = request.args.get('uid')
    user = User.query.get(int(uid))
    if user:
        integral = 0
        lastcheckin = user.lastcheckin

        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        yestoday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
        print yestoday
        checkinrecord = CheckinRecord()
        checkinrecord.uid = uid
        checkinrecord.timestamp = now
        user.lastcheckin = now

        if lastcheckin and lastcheckin.startswith(yestoday):
            user.continus_checkin += 1
        else:
            user.continus_checkin = 1

        #增加积分
        if user.continus_checkin > 7:
            des = u'连续签到7天'
        else:
            des = u'连续签到%d天' % user.continus_checkin
        integral_strategy = IntegralStrategy.query.filter_by(description=des).first()
        if integral_strategy:
            integral = integral_strategy.value
            user.integral = user.integral + integral_strategy.value
            integral_record = IntegralRecord()
            integral_record.uid = uid
            integral_record.action = integral_strategy.id
            integral_record.change = integral_strategy.value
            integral_record.timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        db.session.add(user)
        db.session.add(checkinrecord)
        db.session.commit()
        return jsonify({
            'code': '0',
            'message': 'success',
            'data':{'integral':integral,'continus_checkin':user.continus_checkin}
        })
    else:
        return jsonify({
            'code': '105',
            'message': 'user not exist',
            'data':None
        })

@auth.route('/reset', methods=['GET','POST'])
def reset_password():
    resetform = ResetForm()
    #resetsubmitform = ResetSubmitForm()
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
        if action == 'reset':
            phonenum = request.form.get('phonenum')
            password = request.form.get('password')
            user = User.query.filter_by(phonenum=phonenum).first()
            user.password = password
            db.session.add(user)
            db.session.commit()
            return jsonify({
                'phonenum': phonenum,
                'password':password
            })
        else:
            phonenum = request.form.get('phonenum')
            vercode = request.form.get('vercode')
            if vercode == cache.get(phonenum):
                return render_template('safety.html',phonenum=phonenum)
            else:
                flash(u'验证码输入错误', 'reset')

        return render_template('reset.html', form=resetform)
    return render_template('reset.html',form=resetform)

@auth.before_app_request
def before_request():
    if session.get('user_id') and not session.get('phonenum'):
        user = User.query.get(int(session.get('user_id')))
        if user:
            print user.phonenum
            #login_user(user, True)
            relation = OrderRelation.query.filter_by(phonenum=user.phonenum).all()
            for r in relation:
                if r.status == '1':
                    session[r.productid] = 1
            session['phonenum'] = user.phonenum
