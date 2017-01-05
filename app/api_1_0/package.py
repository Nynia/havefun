from app import app
from flask import request,jsonify
from app.models import Package
from app import db
import datetime

@app.route('/api/v1/packages/<id>', methods=['GET'])
def get_package_by_id(id):
    package = Package.query.get(id)
    return jsonify({
        'code': '0',
        'messge': 'success',
        'data': package.to_json() if package else package
    })

@app.route('/api/v1/packages', methods=['GET'])
def get_packages_by_type():
    type = request.args.get('type')
    packages = Package.query.filter_by(type=type).all()
    return jsonify({
        'code': '0',
        'messge': 'success',
        'data': [p.to_json() for p in packages]
    })

@app.route('/api/v1/packages', methods=['POST'])
def add_package():
    packageid = request.form['packageid']
    package = Package.query.get(packageid)
    if package == None:
        package = Package()
        package.packageid = packageid
        package.packagename = request.form['packagename']
        package.type = request.form['type']
        package.price = request.form['price']
        package.description = request.form['description']
        package.createtime = datetime.datetime.now()
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

@app.route('/api/v1/packages/<id>', methods=['PUT'])
def update_package_by_id(id):
    package = Package.query.get(id)
    if package:
        if request.form.has_key('packagename'):
            package.packagename = request.form['packagename']
        if request.form.has_key('type'):
            package.type = request.form['type']
        if request.form.has_key('price'):
            package.price = request.form['price']
        if request.form.has_key('description'):
            package.description = request.form['description']
        package.modifiedtime = datetime.datetime.now()
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

@app.route('/api/v1/packages/<id>', methods=['DELETE'])
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

