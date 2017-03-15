from . import api
from flask import request, jsonify, session
from app.models import OrderRelation,OrderHistroy

@api.route('/records', methods=['GET'])
def get_record():
    productid = request.args.get('productid')
    phonenum = request.args.get('phonenum')
    action = request.args.get('action')
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')


    records = OrderHistroy.query
    if productid:
        records = records.filter_by(productid=productid)
    if phonenum:
        records = records.filter_by(phonenum=phonenum)
    if action:
        records = records.filter_by(action=action)
    if starttime:
        records = records.filter(OrderHistroy.createtime>=starttime)
    if endtime:
        records = records.filter(OrderHistroy.createtime<=endtime)

    records = records.all()
    return jsonify({
        'code': '0',
        'message': 'success',
        'data': [r.to_json() for r in records]
    })