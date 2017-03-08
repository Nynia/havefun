from . import api
from app import db
from flask import request,jsonify
from app.models import Game
from datetime import datetime
from decorators import jsonp

@api.route('/games',methods=['GET'])
@jsonp
def get_games_by_type():
    type = request.args.get('type')
    packageid = request.args.get('packageid')
    category = request.args.get('category')

    if type and packageid:
        return jsonify({
            'code': '103',
            'message': 'params error',
            'data': None
        })
    elif type:
        games = Game.query.filter_by(type=type)
        if type == '2' and category:
            games = games.filter_by(category=category).all()
        games = games.order_by(Game.star).all()
    elif packageid:
        games = Game.query.filter_by(packageid=packageid).all()
    else:
        games = Game.query.all()
    return jsonify({
        'code': '0',
        'message': 'success',
        'data': [g.to_json() for g in games]
    })


@api.route('/games/<id>',methods=['GET'])
@jsonp
def get_game_by_id(id):
    game = Game.query.get(int(id))
    if game:
        return jsonify({
            'code': '0',
            'message': 'success',
            'data': game.to_json()
        })
    else:
        return jsonify({
            'code': '102',
            'messge': 'not exist',
            'data': None
        })

@api.route('/games',methods=['POST'])
@jsonp
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
@jsonp
def update_game_by_id(id):
    game = Game.query.get(int(id))
    if game:
        print type(request.form)
        for key,value in request.form.items():
            if hasattr(game, key):
                setattr(game, key, value)
            else:
                return jsonify({
                    'code': '103',
                    'message': 'params error',
                    'data': None
                })
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
@jsonp
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
















