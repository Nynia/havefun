# -*- coding: UTF-8 -*-
from . import api
from flask import request, jsonify, session
from urllib import quote
import hashlib
from app.models import OrderRelation, OrderHistroy, Package, IntegralStrategy, IntegralRecord, User


@api.route('/tyzone/callback', methods=['POST', 'GET'])
def func():
    print session.get('phonenum')
    apsecret = '2027e1d246f3aa52f1c6ea786cc4ef4e'
    params = []
    sig2 = ''
    print request.form.to_dict()
    for key, value in request.form.to_dict().items():
        if key != 'sig2':
            params.append((key, value))
        else:
            sig2 = value
    sorted_params = sorted(params)
    print sorted_params
    key_str = ''
    for params in sorted_params:
        if params[1] != '':
            key_str += params[0]
            key_str += params[1]
    print key_str

    # key_quoted = quote(key_str)
    # print key_quoted
    # print sig2, hashlib.sha1(key_quoted + apsecret).hexdigest()
    # if sig2 == hashlib.sha1(key_quoted + apsecret).hexdigest():
    #     return jsonify({
    #         'resultCode': '0000',
    #         'resultDesc': 'accepted'
    #     })
    # else:
    #     return jsonify({
    #         'resultCode': '0001',
    #         'resultDesc': 'accept error'
    #     })
    # orderrelation = OrderRelation.query.filter_by(phonenum=phonenum).filter_by(productid=productid).first()
    # if not orderrelation:
    #     orderrelation = OrderRelation()
    #
    # orderhistory = OrderHistroy()
    # orderaction.productid = productid
    # orderaction.phonenum = phonenum
    # orderhistory.productid = productid
    # orderhistory.phonenum = phonenum
    # orderrelation.ordertime = timestamp
    # orderrelation.status = '1'
    #
    # orderhistory.action = '1'
    # orderhistory.createtime = timestamp
    #
    # user = User.query.filter_by(phonenum=phonenum).first()
    # des = ''
    # record = IntegralRecord.query.filter_by(uid=user.id).filter_by(action=9).first()
    # if not record:
    #     des = u'首次订购付费包'
    # else:
    #     des = u'订购付费包'
    #
    # # integral
    # integral_strategy = IntegralStrategy.query.filter_by(description=des).first()
    # if integral_strategy:
    #     integral = integral_strategy.value
    #     user = User.query.filter_by(phonenum=phonenum).first()
    #     if integral_strategy.id == 7:
    #         user.integral = user.integral + integral_strategy.value
    #         integral_record = IntegralRecord()
    #         integral_record.uid = user.id
    #         integral_record.action = integral_strategy.id
    #         integral_record.change = integral_strategy.value
    #         integral_record.timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    #         db.session.add(user)
    #         db.session.add(integral_record)
    #     else:
    #         today = datetime.now().strftime('%Y%m%d')
    #         record = IntegralRecord.query.filter(timestamp.startswith(today)).filter_by(action=8).all()
    #         history_integral_today = 0
    #         if record:
    #             history_integral_today = 400 + reduce(lambda x, y: x + y, [r.change for r in record])
    #             print history_integral_today
    #         if history_integral_today < 600:
    #             user.integral = user.integral + integral_strategy.value
    #             integral_record = IntegralRecord()
    #             integral_record.uid = user.id
    #             integral_record.action = integral_strategy.id
    #             integral_record.change = integral_strategy.value
    #             integral_record.timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    #             db.session.add(user)
    #             db.session.add(integral_record)
    # db.session.add(orderrelation)
    # db.session.add(orderhistory)
    # db.session.commit()
    #
    # session[productid] = 1
    return jsonify({
        'resultCode': '0000',
        'resultDesc': 'accepted'
    })
