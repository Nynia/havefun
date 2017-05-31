from . import api
from flask import request, jsonify
from app.models import User
from app import db
from datetime import datetime

@api.route('/users/<id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    return jsonify({
        'code': '0',
        'message': 'success',
        'data': user.to_json() if user else user
    })

@api.route('/users', methods=['GET'])
def get_users_by_page():
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int)
    if not offset:
        offset = 0
    if not limit:
        limit = 20
    users = User.query.offset(offset=offset).limit(limit=limit).all()
    return jsonify({
        'code': '0',
        'messge': 'success',
        'data': [u.to_json() for u in users]
    })

@api.route('/users', methods=['POST'])
def add_user():
    phonenum = request.form.get('phonenum')
    user = User.query.filter_by(phonenum=phonenum).first()
    if not user:
        user = User()
        user.phonenum = phonenum
        user.password = request.form.get('password')
        user.nickname = request.form.get('nickname')
        user.integral = 0
        user.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'code': '0',
            'message': 'success',
            'data': user.to_json()
        })
    else:
        return jsonify({
            'code': '101',
            'message': 'exist',
            'data': user.to_json()
        })

@api.route('/users/<id>', methods=['PUT'])
def update_user_by_id(id):
    user = User.query.get(id)
    if user:
        for key,value in request.form.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'code': '0',
            'message': 'success',
            'data': user.to_json()
        })
    else:
        return jsonify({
            'code': '102',
            'msssage': 'not exist',
            'data': None
        })

@api.route('/users/<id>', methods=['DELETE'])
def delete_user_by_id(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            'code': '0',
            'message': 'success',
            'data': user.to_json()
        })
    else:
        return jsonify({
            'code': '102',
            'message': 'not exist',
            'data': None
        })