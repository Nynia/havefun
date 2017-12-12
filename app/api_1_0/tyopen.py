# -*-coding:utf-8-*-
from . import api
from flask import request, jsonify,session,redirect,url_for
import time,json
import requests
from ..models import User,OrderRelation,IntegralStrategy
from flask_login import login_user,current_user
from app import db

CLIENT_ID = '8148610453'
APP_SECRET = 'DeAEsBOFlMuhPoCkJqGAniMqthO1q5dK'

@api.route('/tyopen/callback', methods=['POST'])
def getuserinfo():
    accessToken = request.form.get('tyAccountToken')
    loginMode = request.form.get('tyloginMode')

    print accessToken, loginMode
    data = {
        'clientId': CLIENT_ID,
        'timestamp': str(int(round(time.time() * 1000))),
        'accessToken': accessToken,
        'version': 'v1.5',
        'clientIp': '127.0.0.1',
    }

    print data
    url = 'https://open.e.189.cn/api/oauth2/account/userInfo.do'
    r = requests.post(url, data=data)
    json_r=  json.loads(r.text)
    print json_r
    #login
    mobileName = json_r['mobileName']
    user = User.query.filter_by(phonenum=mobileName).first()
    if user is None:
        #register
        from datetime import datetime
        user = User()
        user.phonenum = mobileName
        user.password = '12345678'
        integral_strategy = IntegralStrategy.query.filter_by(description=u'注册帐号').first()
        user.integral = integral_strategy.value
        user.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
        db.session.add(user)
        db.session.commit()
    #login
    print user
    login_user(user, True)
    print current_user
    relation = OrderRelation.query.filter_by(phonenum=user.phonenum).all()
    for r in relation:
        if r.status == '1':
            session[r.productid] = 1
    session['phonenum'] = user.phonenum
    print session
    print session.get('user_id')

    #return
    return jsonify({
        'code': '0',
        'message': 'success'
    })