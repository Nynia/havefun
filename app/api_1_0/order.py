from . import api
from app import db
from flask import request, jsonify, session
from datetime import datetime
from config import ORDER_REQUEST_URL
import hashlib, json
from app.models import OrderRelation,OrderHistroy,Package
import requests

@api.route('/orders', methods=['POST'])
def orderaction():
    action = request.args.get('action')
    spid = request.form.get('spid')
    chargeid = request.form.get('chargeid')
    secret = request.form.get('secret')
    productid = request.form.get('productid')
    phonenum = request.form.get('phonenum')
    if action:
        if spid and chargeid and secret and phonenum:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            token = hashlib.sha1(chargeid + timestamp + secret).hexdigest()
            data = {
                'action': action,
                'spId': spid,
                'chargeId': chargeid,
                'phoneNum': phonenum,
                'orderType': '1',
                'timestamp': timestamp,
                'accessToken': token
            }
            r = requests.post(ORDER_REQUEST_URL, data=data)
            json_result = json.loads(r.text)
            print json_result
            err_code = json_result['errcode']
            err_msg = json_result['errmsg']
            if err_code == '0':
                orderaction = OrderRelation.query.filter_by(phonenum=phonenum).filter_by(productid=productid).first()
                if not orderaction:
                    orderaction = OrderRelation()
                orderhistory = OrderHistroy()
                orderaction.productid = productid
                orderaction.phonenum = phonenum
                orderhistory.productid = productid
                orderhistory.phonenum = phonenum
                if action == 'subscribe':
                    orderaction.starttime = timestamp
                    orderaction.status = '1'
                    orderhistory.action = '1'
                    orderhistory.createtime = timestamp
                else:
                    orderaction.endtime = timestamp
                    orderaction.status = '4'
                    orderhistory.action = '0'
                    orderhistory.createtime = timestamp

                db.session.add(orderaction)
                db.session.add(orderhistory)
                db.session.commit()

                return jsonify({
                    'code': err_code,
                    'message': err_msg,
                    'data': None
                })

            else:
                return jsonify({
                    'code': err_code,
                    'message': err_msg,
                    'data': None
                })
        else:
            return jsonify({
                'code': '103',
                'message': 'params error',
                'data': None
            })

    else:
        return jsonify({
            'code': '103',
            'message': 'params error',
            'data':None
        })


@api.route('/orders/<phonenum>', methods=['GET'])
def checkstatus(phonenum):
    productid = request.args.get('productid')
    relations = OrderRelation.query.filter_by(phonenum=phonenum)
    if productid:
        relations = relations.filter_by(productid=productid).all()
    else:
        relations = relations.all()
    if relations:
        return jsonify({
            'code': '0',
            'message': 'success',
            'data': [r.to_json() for r in relations]
        })
    else:
        return jsonify({
            'code': '102',
            'message': 'not exist',
            'data': None
        })

@api.route('/subscribe', methods=['POST'])
def subscribe():
    productid = request.form.get('productid')
    phonenum = request.form.get('phonenum')
    package = Package.query.get(productid)
    chargeid = package.chargeid
    secret = package.secret
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    token = hashlib.sha1(chargeid + timestamp + secret).hexdigest()
    data = {
        'action': 'subscribe',
        'spId': package.spid,
        'chargeId': package.chargeid,
        'phoneNum': phonenum,
        'orderType': '1',
        'timestamp': timestamp,
        'accessToken': token
    }
    r = requests.post('http://61.160.185.51:9250/ismp/serviceOrder', data=data)
    json_result = json.loads(r.text)
    print json_result
    err_code = json_result['errcode']
    err_msg = json_result['errmsg']
    if err_code == '0':
        orderaction = OrderRelation.query.filter_by(phonenum=phonenum).filter_by(productid=productid).first()
        if not orderaction:
            orderaction = OrderRelation()
        orderhistory = OrderHistroy()
        orderaction.productid = productid
        orderaction.phonenum = phonenum
        orderhistory.productid = productid
        orderhistory.phonenum = phonenum
        orderaction.ordertime = timestamp
        orderaction.status = '1'

        orderhistory.action = '1'
        orderhistory.createtime = timestamp

        db.session.add(orderaction)
        db.session.add(orderhistory)
        db.session.commit()

        session[productid] = 1

        return jsonify({
            'code': err_code,
            'message': err_msg,
            'data': None
        })

    else:
        return jsonify({
            'code': err_code,
            'message': err_msg,
            'data': None
        })

@api.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    productid = request.form.get('productid')
    phonenum = request.form.get('phonenum')
    package = Package.query.get(productid)
    chargeid = package.chargeid
    secret = package.secret
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    token = hashlib.sha1(chargeid + timestamp + secret).hexdigest()
    data = {
        'action': 'unsubscribe',
        'spId': package.spid,
        'chargeId': package.chargeid,
        'phoneNum': phonenum,
        'orderType': '1',
        'timestamp': timestamp,
        'accessToken': token
    }
    r = requests.post('http://61.160.185.51:9250/ismp/serviceOrder', data=data)
    json_result = json.loads(r.text)
    print json_result
    err_code = json_result['errcode']
    err_msg = json_result['errmsg']
    if err_code == '0':
        orderaction = OrderRelation.query.filter_by(phonenum=phonenum).filter_by(productid=productid).first()
        if not orderaction:
            orderaction = OrderRelation()
        orderhistory = OrderHistroy()
        orderaction.productid = productid
        orderaction.phonenum = phonenum
        orderhistory.productid = productid
        orderhistory.phonenum = phonenum

        orderaction.canceltime = timestamp
        orderaction.status = '4'
        orderhistory.action = '0'
        orderhistory.createtime = timestamp

        db.session.add(orderaction)
        db.session.add(orderhistory)
        db.session.commit()

        session.pop(productid)

        return jsonify({
            'code': err_code,
            'message': err_msg,
            'data': None
        })

    else:
        return jsonify({
            'code': err_code,
            'message': err_msg,
            'data': None
        })

