from . import api
from app import db
from flask import request,jsonify
from app.models import Game
from datetime import datetime


@api.route('/games',methods=['GET'])
def get_games_by_type():
    type = request.args.get('type')
    if type:
        games = Game.query.filter_by(type=type).all()
    else:
        games = Game.query.all()
    return jsonify({
        'code': '0',
        'message': 'success',
        'data': [g.to_json() for g in games]
    })

@api.route('/games/<id>',methods=['GET'])
def get_game_by_id(id):
    game = Game.query.get(int(id))
    return jsonify({
        'code': '0',
        'message': 'success',
        'data': game.to_json() if game else game
    })

@api.route('/games',methods=['POST'])
def add_new_game():
    game = Game()
    for key, value in request.form.items():
        if hasattr(game, key):
            setattr(game, key, value)
    game.createtime = datetime.now().strftime('%Y%m%d%H%M%S')

    db.session.add(game)
    db.session.commit()
    return jsonify({
        'code': '0',
        'message': 'success',
        'data': game.to_json()
    })

@api.route('/games/<id>',methods=['PUT'])
def update_game_by_id(id):
    game = Game.query.get(int(id))
    if game:
        print type(request.form)
        for key,value in request.form.items():
            if hasattr(game, key):
                setattr(game, key, value)
        db.session.add(game)
        db.session.commit()
        return jsonify({
            'code': '0',
            'message': 'success',
            'data': game.to_json()
        })

    else:
        return jsonify({
            'code': '102',
            'msssage': 'not exist',
            'data': None
        })

@api.route('/games/<id>', methods=['DELETE'])
def delete_by_id(id):
    game = Game.query.get(int(id))
    if game:
        db.session.delete(game)
        db.session.commit()
        return jsonify({
            'code':'0',
            'message':'success',
            'data':game.to_json()
        })
    else:
        return jsonify({
            'code':'102',
            'message':'not exist',
            'data':None
        })
















