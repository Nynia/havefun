from . import api
from flask import request,jsonify
from app.models import Reading,Chapter
from app import db
from datetime import datetime

@api.route('/readings/<id>', methods=['GET'])
def get_reading_by_id(id):
    reading = Reading.query.get(int(id))
    if reading:
        return jsonify({
            'code': '0',
            'message': 'success',
            'data': reading.to_json()
        })
    else:
        return jsonify({
            'code': '102',
            'message': 'not exist',
            'data': None
        })
@api.route('/readings', methods=['POST'])
def add_new_reading():
    bookid = request.form.get('bookid')
    book = Reading.query.filter_by(bookid=bookid).first()
    if book == None:
        book = Reading()
        book.bookid = bookid
        for key, value in request.form.items():
            if hasattr(book, key):
                setattr(book, key, value)
        book.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
        book.modifiedtime = datetime.now().strftime('%Y%m%d%H%M%S')
        db.session.add(book)
        db.session.commit()
        return jsonify({
            'code': '0',
            'message': 'success',
            'data': book.to_json()
        })
    else:
        return jsonify({
            'code': '101',
            'message': 'exist',
            'data': book.to_json()
        })
@api.route('/readings/<id>', methods=['PUT'])
def update_reading(id):
    book = Reading.query.get(int(id))
    if book == None:
        for key,value in request.form.items():
            if hasattr(book, key):
                setattr(book, key, value)
        book.modifiedtime = datetime.now().strftime('%Y%m%d%H%M%S')
        db.session.add(book)
        db.session.commit()
        return jsonify({
            'code': '0',
            'message': 'success',
            'data': book.to_json()
        })
    else:
        return jsonify({
            'code': '102',
            'message': 'not exist',
            'data': book.to_json()
        })

@api.route('/readings/<id>', methods=['DELETE'])
def delete_reading(id):
    book = Reading.query.get(int(id))
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({
            'code': '0',
            'message': 'success',
            'data': book.to_json()
        })
    else:
        return jsonify({
            'code': '102',
            'message': 'not exist',
            'data': None
        })

@api.route('/readings/bookid/<id>', methods=['GET'])
def get_chapter():
    pass