from . import api
from app import db
from flask import request,jsonify
from app.models import Comic,ComicChapterInfo
from datetime import datetime
from decorators import jsonp

@api.route('/comics', methods=['GET'])
@jsonp
def get_comics_by_package():
   packageid = request.args.get('packageid')
   comics = Comic.query.filter_by(packageid=packageid).all()
   return jsonify({
        'code':'0',
        'message':'success',
        'data':[c.to_json() for c in comics]
   })

@api.route('/comics/<id>', methods=['GET'])
@jsonp
def get_comic_by_id(id):
    comic = Comic.query.get(int(id))
    return jsonify({
        'code':'0',
        'message':'success',
        'data':comic.to_json() if comic else comic
    })

@api.route('/comics', methods=['POST'])
@jsonp
def add_comic():
    id = request.form['id']
    comic = Comic.query.get(id)
    if comic == None:
        comic = Comic()
        comic.id = id
        for key, value in request.form.items():
            if hasattr(comic, key):
                setattr(comic, key, value)

        comic.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
        comic.recentupdatetime = datetime.now().strftime('%Y%m%d%H%M%S')
        comic.modifiedtime = datetime.now().strftime('%Y%m%d%H%M%S')

        db.session.add(comic)
        db.session.commit()
        return jsonify({
            'code':'0',
            'message':'success',
            'data':comic.to_json()
        })
    else:
        return jsonify({
            'code':'101',
            'message':'exist',
            'data':comic.to_json()
        })

@api.route('/comics/<id>', methods=['PUT'])
@jsonp
def update_comic_by_id(id):
    comic = Comic.query.get(int(id))
    if comic:
        for key,value in request.form.items():
            if hasattr(comic, key):
                setattr(comic, key, value)
        comic.modifiedtime = datetime.datetime.now()
        db.session.add(comic)
        db.session.commit()
        return jsonify({
            'code':'0',
            'message':'success',
            'data':comic.to_json()
        })
    else:
        return jsonify({
            'code':'102',
            'msssage':'not exist',
            'data':None
        })
@api.route('/comics/<id>', methods=['DELETE'])
@jsonp
def delete_comic_by_id(id):
    comic = Comic.query.get(int(id))
    if comic:
        db.session.delete(comic)
        db.session.commit()
        return jsonify({
            'code':'0',
            'message':'success',
            'data':comic.to_json()
        })
    else:
        return jsonify({
            'code':'102',
            'message':'not exist',
            'data':None
        })

@api.route('/comics/chapters/<id>', methods=['POST'])
def add_chapter_by_id(id):
    chapterinfo = ComicChapterInfo()
    chapterinfo.bookid = id
    chapterinfo.chapterid = request.form.get('chapterid')
    chapterinfo.quantity = request.form.get('quantity')

    chapterinfo.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
    chapterinfo.updatetime = datetime.now().strftime('%Y%m%d%H%M%S')

    db.session.add(chapterinfo)
    db.session.commit()

    return jsonify({
        'code':'0',
        'message':'succss',
        'data':chapterinfo.to_json()
    })