from . import api
from app import db
from flask import request,jsonify
from app.models import IntegralStrategy
from datetime import datetime

@api.route('/integral/strategy', methods=['POST'])
def add_new_strategy():
    value = request.form.get('value')
    description = request.form.get('description')
    strategy = IntegralStrategy()
    strategy.value = value
    strategy.description = description
    strategy.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
    strategy.updatetime = datetime.now().strftime('%Y%m%d%H%M%S')

    db.session.add(strategy)
    db.session.commit()

    return jsonify({
        'code':'0',
        'message':'success',
        'data':strategy.to_json()
    })

