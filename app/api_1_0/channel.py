from . import api
from flask import request, jsonify
from app import db
from app.models import Channel
from datetime import datetime
from app.utils.func import generate_channel_token


@api.route('/channel', methods=['GET'])
def add_channel():
    name = request.args.get('name')
    print name
    if name != None:
        channel = Channel()
        channel.name = name
        channel.status = '1'
        channel.createtime = datetime.now().strftime('%Y%m%d')
        token = generate_channel_token(name)
        channel.token = token

        db.session.add(channel)
        db.session.commit()

        return jsonify({
            'code': '0',
            'message': 'success',
            'token': token
        })
    else:
        return jsonify({
            'code': '101',
            'message': 'params error'
        })
