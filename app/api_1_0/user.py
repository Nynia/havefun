from app import app
from flask import request, jsonify
from app.models import User
from app import db
import datetime

@app.route('/api/v1/users/<id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    return jsonify({
        'code': '0',
        'message': 'success',
        'data': user.to_json() if user else user
    })

@app.route('/api/v1/users', methods=['GET'])
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

@app.route('/api/v1/users', methods=['POST'])
def add_user():
    phonenum = request.form['phonenum']
    print phonenum
    user = User.query.filter_by(phonenum=phonenum).first()
    if not user:
        user = User()
        user.phonenum = phonenum
        user.password = request.form['password']
        user.nickname = request.form['nickname']
        user.integral = 0
        user.createtime = datetime.datetime.now()
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

@app.route('/api/v1/users/<id>', methods=['PUT'])
def update_user_by_id(id):
    user = User.query.get(id)
    if user:
        if request.form.has_key('nickname'):
            user.nickname = request.form['nickname']
        if request.form.has_key('password'):
            user.password = request.form['password']
        if request.form.has_key('phonenum'):
            user.phonenum = request.form['phonenum']
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

@app.route('/api/v1/users/<id>', methods=['DELETE'])
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