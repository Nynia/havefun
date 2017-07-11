# -*-coding=utf-8-*-
from . import api
from app import db
from flask import request,jsonify
from app.models import FavorInfo,Game,Comic,IntegralRecord,IntegralStrategy,User
from datetime import datetime

@api.route('/favors/<uid>',methods=['GET'])
def get_favors_by_uid(uid):
    type = request.args.get('type')
    favorinfos = FavorInfo.query.filter_by(uid=uid).filter_by(type=type).all()
    return jsonify({
        'code': '0',
        'message': 'success',
        'data': [c.to_json() for c in favorinfos]
    })

@api.route('/favors/favor',methods=['GET'])
def favor():
    uid = request.args.get('uid')
    cid = request.args.get('cid')
    type = request.args.get('type')

    integral = 0
    if type == '1':
        comic = Comic.query.get(int(cid))
        if not comic:
            return jsonify({
                'code': '108',
                'message': 'comic not exist',
                'data': None
            })
    elif type == '2':
        game = Game.query.get(int(cid))
        if not game:
            return jsonify({
                'code': '109',
                'message': 'game not exist',
                'data': None
            })
    else:
        return jsonify({
            'code': '110',
            'message': 'type error',
            'data': None
        })
    user = User.query.get(int(uid))
    if not user:
        return jsonify({
            'code': '111',
            'message': 'user not exist',
            'data': None
        })
    favorinfo = FavorInfo.query.filter_by(uid=uid).filter_by(cid=cid).first()
    if favorinfo:
        favorinfo.state = '1'
        favorinfo.updatetime = datetime.now().strftime('%Y%m%d%H%M%S')
    else:
        favorinfo = FavorInfo()
        favorinfo.uid = uid
        favorinfo.cid = cid
        favorinfo.type = type
        favorinfo.state = '1'
        favorinfo.updatetime = datetime.now().strftime('%Y%m%d%H%M%S')

        integral_strategy = IntegralStrategy.query.filter_by(description=u'收藏').first()
        if integral_strategy:
            today = datetime.now().strftime('%Y%m%d')
            integral_history = IntegralRecord.query.filter(IntegralRecord.timestamp.startswith(today)).filter_by(
                action=integral_strategy.id).all()
            history_integral_today = 0
            if integral_history:
                history_integral_today = reduce(lambda x, y: x + y, [r.change for r in integral_history])
                print history_integral_today
            if history_integral_today < 80:
                integral = integral_strategy.value
                user.integral = user.integral + integral_strategy.value
                integral_record = IntegralRecord()
                integral_record.uid = uid
                integral_record.action = integral_strategy.id
                integral_record.change = integral_strategy.value
                integral_record.timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                db.session.add(user)
                db.session.add(integral_record)
    db.session.add(favorinfo)
    db.session.commit()
    return jsonify({
        'code': '0',
        'message': 'success',
        'data': {
            'integral':integral
        }
    })

@api.route('/favors/unfavor',methods=['GET'])
def unfavor():
    uid = request.args.get('uid')
    cid = request.args.get('cid')
    type = request.args.get('type')

    favorinfo = FavorInfo.query.filter_by(uid=uid).filter_by(cid=cid).first()
    if favorinfo:
        favorinfo.state = '0'
        favorinfo.updatetime = datetime.now().strftime('%Y%m%d%H%M%S')
    else:
        return jsonify({
            'code': '107',
            'message': 'not favored',
            'data': None
        })

    db.session.add(favorinfo)
    db.session.commit()
    return jsonify({
        'code': '0',
        'message': 'success',
        'data': favorinfo.to_json()
    })

@api.route('/favors',methods=['GET'])
def is_favored():
    cid = request.args.get('cid')
    type = request.args.get('type')
    uid = request.args.get('uid')

    favored = FavorInfo.query.filter_by(uid=uid).filter_by(cid=cid).filter_by(type=type).first()
    if favored and favored.state == '1':
        favored = True
    else:
        favored = False
    favor_count = FavorInfo.query.filter_by(cid=cid).filter_by(type=type).filter_by(state='1').count()

    print favored,favor_count
    return jsonify({
        'code':'0',
        'message':'success',
        'data':{
            'favored': favored,
            'favor_count': 1500+favor_count
        }
    })
