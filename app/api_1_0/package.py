from . import api
from flask import request,jsonify
from app.models import Package
from app import db
from datetime import datetime

@api.route('/packages/<id>', methods=['GET'])
def get_package_by_id(id):
    package = Package.query.get(int(id))
    if package:
        return jsonify({
            'code': '0',
            'message': 'success',
            'data': package.to_json()
        })
    else:
        return jsonify({
            'code': '102',
            'message': 'not exist',
            'data': None
        })
@api.route('/packages', methods=['GET'])
def get_packages_by_type():
    type = request.args.get('type')
    if type:
        packages = Package.query.filter_by(type=type).all()
    else:
        packages = Package.query.all()
    return jsonify({
        'code': '0',
        'message': 'success',
        'data': [p.to_json() for p in packages]
    })

@api.route('/packages', methods=['POST'])
def add_package():
    productid = request.form.get('productid')
    package = Package.query.filter_by(productid=productid).first()
    if package == None:
        package = Package()
        package.productid = productid
        for key, value in request.form.items():
            if hasattr(package, key):
                setattr(package, key, value)
        package.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
        package.modifiedtime = datetime.now().strftime('%Y%m%d%H%M%S')
        db.session.add(package)
        db.session.commit()
        return jsonify({
            'code':'0',
            'message':'success',
            'data':package.to_json()
        })
    else:
        return jsonify({
            'code': '101',
            'message': 'exist',
            'data': package.to_json()
        })

@api.route('/packages/<id>', methods=['PUT'])
def update_package_by_id(id):
    package = Package.query.get(id)
    if package:
        for key,value in request.form.items():
            if hasattr(package, key):
                setattr(package, key, value)
        package.modifiedtime = datetime.now().strftime('%Y%m%d%H%M%S')
        db.session.add(package)
        db.session.commit()
        return jsonify({
            'code': '0',
            'message': 'success',
            'data': package.to_json()
        })
    else:
        return jsonify({
            'code': '102',
            'message': 'not exist',
            'data': None
        })

@api.route('/packages/<id>', methods=['DELETE'])
def delete_package_by_id(id):
    package = Package.query.get(id)
    if package:
        db.session.delete(package)
        db.session.commit()
        return jsonify({
            'code': '0',
            'message': 'success',
            'data': package.to_json()
        })
    else:
        return jsonify({
            'code': '102',
            'message': 'not exist',
            'data': None
        })

