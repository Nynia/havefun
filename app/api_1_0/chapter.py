from . import api
from flask import request,jsonify
from app.models import Chapter
from app import db
from datetime import datetime
from decorators import jsonp

@api.route('/chapters', methods=['GET','POST'])
def add_chapter():
    chapterid = request.form.get('chapterid')
    chaptername = request.form.get('chaptername')
    bookid = request.form.get('bookid')
    content = request.form.get('content')

    chapter = Chapter()
    chapter.bookid = bookid
    chapter.chapterid = chapterid
    chapter.content = content
    chapter.chaptername = chaptername

    chapter.createtime = datetime.now().strftime('%Y%m%d%H%M%S')

    db.session.add(chapter)
    db.session.commit()

    return jsonify({
        'code': '0',
        'message': 'success',
        'data': chapter.to_json()
    })