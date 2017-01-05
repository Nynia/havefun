from app import app,db
from flask import request,jsonify
from app.models import Comic
import datetime

@app.route('/api/v1/comics', methods=['GET'])
def get_all_comics():
   comics = Comic.query.all()
   return jsonify({
        'code':'0',
        'message':'success',
        'data':[c.to_json() for c in comics]
   })

@app.route('/api/v1/comics/<id>', methods=['GET'])
def get_comic_by_id(id):
    comic = Comic.query.get(id)
    return jsonify({
        'code':'0',
        'message':'success',
        'data':comic.to_json() if comic else comic
    })

@app.route('/api/v1/comics', methods=['POST'])
def add_comic():
    comicid = request.form['comicid']
    comic = Comic.query.get(comicid)
    if comic == None:
        comic = Comic()
        comic.comicid = comicid
        comic.comicname = request.form['comicname']
        comic.packageid = request.form['packageid']
        comic.brief = request.form['brief']
        comic.author = request.form['author']
        comic.category = request.form['category']
        comic.hits = request.form['hits']
        comic.state = request.form['state']
        comic.cover = request.form['cover']
        comic.curchapter = request.form['curchapter']
        comic.freechapter = request.form['freechapter']
        comic.createtime = datetime.datetime.now()
        comic.recentupdatetime = datetime.datetime.now()
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
            'code':'101',
            'message':'exist',
            'data':comic.to_json()
        })

@app.route('/api/v1/comics/<id>', methods=['PUT'])
def update_comic_by_id(id):
    comic = Comic.query.get(id)
    if comic:
        if request.form.has_key('comicname'):
            comic.comicname = request.form['comicname']
        if request.form.has_key('packageid'):
            comic.packageid = request.form['packageid']
        if request.form.has_key('brief'):
            comic.brief = request.form['brief']
        if request.form.has_key('author'):
            comic.author = request.form['author']
        if request.form.has_key('category'):
            comic.category = request.form['category']
        if request.form.has_key('hits'):
            comic.hits = request.form['hits']
        if request.form.has_key('state'):
            comic.state = request.form['state']
        if request.form.has_key('cover'):
            comic.cover = request.form['cover']
        if request.form.has_key('freechapter'):
            comic.freechapter = request.form['freechapter']
        if request.form.has_key('curchapter'):
            comic.curchapter = request.form['curchapter']
            comic.recentupdatetime = datetime.datetime.now()
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
@app.route('/api/v1/comics/<id>', methods=['DELETE'])
def delete_comic_by_id(id):
    comic = Comic.query.get(id)
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

@app.route('/api/v1/comics/chapters/<id>', methods=['GET'])
def get_chapter_by_id(id):
    pass