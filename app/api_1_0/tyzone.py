# -*- coding: UTF-8 -*-
from . import api
from flask import request, jsonify, session
from app import redis_cli, db
from urllib import quote_plus
import hashlib
from app.models import OrderRelation, OrderHistroy, Package, IntegralStrategy, IntegralRecord, User
from datetime import datetime


@api.route('/tyzone/clientcall', methods=['POST'])
def clientcall():
    print session
    phonenum = request.form.get('phonenum')
    result_code = request.form.get('code')
    orderid = request.form.get('orderid')
    print phonenum, result_code, orderid
    redis_cli.set(orderid, phonenum)
    return phonenum


@api.route('/tyzone/callback', methods=['POST', 'GET'])
def zonecall():
    params = []
    print request.form.to_dict()
    for key, value in request.form.to_dict().items():
        if not key.startswith('sig'):
            params.append((key, value))
    sorted_params = sorted(params)
    print sorted_params
    key_str = ''
    for params in sorted_params:
        if params[1] != '':
            key_str += params[0]
            key_str += params[1]
    print key_str
    orderid = request.form.get('txId')
    paytime = request.form.get('payTime')
    type = request.form.get('chargeType')
    chargeid = request.form.get('chargeId')
    result = request.form.get('chargeResult')
    md5fromnum = request.form.get('md5fromnum')
    print orderid, paytime, type, result, chargeid
    package = Package.query.filter_by(chargeid=chargeid).first()
    if package:
        productid = package.productid
        apsecret = package.secret
        phonenum = redis_cli.get(orderid)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        if result == '-99':
            # 订购成功
            orderhistory = OrderHistroy()
            orderhistory.productid = productid
            orderhistory.phonenum = phonenum
            orderhistory.action = '1'
            orderhistory.createtime = timestamp
            if not phonenum or md5fromnum != hashlib.md5(phonenum).hexdigest().upper():
                print 'phonenum md5 not matched'
                # 只记录订购历史
            else:
                # 更新订购关系及积分
                orderrelation = OrderRelation.query.filter_by(phonenum=phonenum).filter_by(productid=productid).first()
                if not orderrelation:
                    orderrelation = OrderRelation()
                orderrelation.ordertime = timestamp
                orderrelation.status = '1'

                user = User.query.filter_by(phonenum=phonenum).first()
                record = IntegralRecord.query.filter_by(uid=user.id).filter_by(action=9).first()
                if not record:
                    des = u'首次订购付费包'
                else:
                    des = u'订购付费包'
                # integral
                integral_strategy = IntegralStrategy.query.filter_by(description=des).first()
                if integral_strategy:
                    # integral = integral_strategy.value
                    user = User.query.filter_by(phonenum=phonenum).first()
                    if integral_strategy.id == 7:
                        user.integral = user.integral + integral_strategy.value
                        integral_record = IntegralRecord()
                        integral_record.uid = user.id
                        integral_record.action = integral_strategy.id
                        integral_record.change = integral_strategy.value
                        integral_record.timestamp = timestamp
                        db.session.add(user)
                        db.session.add(integral_record)
                    else:
                        today = datetime.now().strftime('%Y%m%d')
                        record = IntegralRecord.query.filter(timestamp.startswith(today)).filter_by(action=8).all()
                        history_integral_today = 0
                        if record:
                            history_integral_today = 400 + reduce(lambda x, y: x + y, [r.change for r in record])
                            print history_integral_today
                        if history_integral_today < 600:
                            user.integral = user.integral + integral_strategy.value
                            integral_record = IntegralRecord()
                            integral_record.uid = user.id
                            integral_record.action = integral_strategy.id
                            integral_record.change = integral_strategy.value
                            integral_record.timestamp = timestamp
                            db.session.add(user)
                            db.session.add(integral_record)
                db.session.add(orderrelation)
                db.session.add(orderhistory)
                db.session.commit()
        elif result == '-100':
            # 退订成功
            orderhistory = OrderHistroy()
            orderhistory.productid = productid
            orderhistory.phonenum = phonenum
            orderhistory.action = '0'
            orderhistory.createtime = timestamp
            if not phonenum or md5fromnum != hashlib.md5(phonenum).hexdigest().upper():
                print 'phonenum md5 not matched'
                # 只记录订购历史
            else:
                # 更新订购关系
                orderrelation = OrderRelation.query.filter_by(phonenum=phonenum).filter_by(productid=productid).first()
                if not orderrelation:
                    orderrelation = OrderRelation()
                orderrelation.canceltime = timestamp
                orderrelation.status = '2'

                db.session.add(orderrelation)
                db.session.add(orderhistory)
                db.session.commit()
    else:
        print 'error: package not found, chargeid: %s' % chargeid
        return jsonify({
            'resultCode': '0001',
            'resultDesc': 'accept error'
        })

    key_quoted = quote_plus(key_str.encode('utf8'))
    print key_quoted
    sig2 = request.form.get('sig2')
    print sig2, hashlib.sha1(key_quoted + apsecret).hexdigest()
    if sig2 == hashlib.sha1(key_quoted + apsecret).hexdigest():
        print 'sig2 matched'
        return jsonify({
            'resultCode': '0000',
            'resultDesc': 'accepted'
        })
