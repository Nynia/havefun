# -*-coding=utf-8-*-
from . import main
from flask import render_template, session, redirect, url_for,jsonify
from .forms import GameForm
from flask import request
from app.api_1_0.game import Game
from werkzeug.utils import secure_filename
import os, re
from app.utils.ftp import MyFTP
from app.utils.func import generate_name
import config
from app import db
from app import myftp
from datetime import datetime
from flask_login import current_user
from app.models import Package, Comic, Reading, Chapter, History


@main.route('/config', methods=['GET', 'POST'])
def config():
    print request.method
    form = GameForm()
    if request.method == 'POST':
        game = Game()
        myftp = MyFTP(config.FTP_ADDR, config.FTP_PORT, config.FTP_USER, config.FTP_PWD, '/')
        myftp.login()
        prefix = config.STATIC_URL_PREFIX
        for key, value in form.data.items():
            if hasattr(game, key):
                setattr(game, key, value)
        file = request.files['icon']
        if file:
            filename = secure_filename(file.filename)
            filename = generate_name(filename)
            print filename
            file.save(os.path.join('./res/', filename))
            myftp.uploadFiles(os.path.join('./res/', filename), '/games/jpg/')
            game.img_icon = prefix + 'games/' + filename
        if form.data['type'] == '1':
            file = request.files['apk']
            if file:
                filename = secure_filename(file.filename)
                filename = generate_name(filename)
                print filename
                file.save(os.path.join('./res/', filename))
                myftp.uploadFiles(os.path.join('./res/', filename), '/games/apk/')
                game.url = prefix + 'games/' + filename
            for index, file in enumerate(request.files.getlist('screenshot')):
                filename = generate_name(secure_filename(file.filename))
                print filename
                file.save(os.path.join('./res/', filename))
                myftp.uploadFiles(os.path.join('./res/', filename), '/games/jpg/')
                setattr(game, 'img_screenshot_' + str(index + 1), prefix + 'games/' + filename)
        game.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
        db.session.add(game)
        db.session.commit()
        print game.to_json()
    return render_template('admin.html', form=form)


@main.route('/game', methods=['GET'])
def game():
    packages = Package.query.filter_by(type=2).all()
    h5 = Game.query.filter_by(type=2).limit(5).all()
    print h5
    return render_template('game.html', packages=packages, h5=h5)


@main.route('/package', methods=['GET'])
def package():
    comicid = request.args.get('comicid')
    bookid = request.args.get('bookid')
    if comicid:
        comic = Comic.query.get(int(comicid))
        id = comic.packageid
    elif bookid:
        reading = Reading.query.filter_by(bookid=bookid).first()
        id = reading.packageid
    else:
        id = request.args.get('id')
    package = Package.query.get(id)
    ordered = False
    print current_user.is_anonymous
    print session.get('phonenum')
    if not current_user.is_anonymous:
        if session.get(package.productid):
            print package.productid
            ordered = True
    if package.type == '1':
        # comic
        comics = Comic.query.filter_by(packageid=id).all()
        return render_template('package_comic.html', package=package, comics=comics, flag=ordered)
    elif package.type == '2':
        # game
        games = Game.query.filter_by(packageid=id).all()
        return render_template('package_game.html', package=package, games=games, flag=ordered)
    elif package.type == '3':
        # music
        pass
    else:
        # reading
        books = Reading.query.filter_by(packageid=id).all()
        print books
        return render_template('package_reading.html', package=package, books=books, flag=ordered)


@main.route('/game/<id>', methods=['GET'])
def gamedetail(id):
    game = Game.query.get(int(id))
    package = Package.query.get(game.packageid)
    flag = False
    if session.get(package.productid):
        flag = True
    return render_template('game_description.html', game=game, flag=flag)


@main.route('/comic', methods=['GET'])
def comic():
    packages = Package.query.filter_by(type=1).all()
    print packages
    return render_template('cartoon.html', packages=packages)


@main.route('/comic/<id>', methods=['GET'])
def comicbrowse(id):
    comic = Comic.query.get(int(id))
    chapter = request.args.get('chapter')
    if request.args.get('type') == 'json':
        if session.get(comic.packageid) or int(chapter) <= comic.freechapter:
            return jsonify({
                'code':'0',
                'msg':chapter
            })
        else:
            return jsonify({
                'code': '1',
                'msg': chapter
            })
    else:
        if chapter == None:
            return render_template('cartoon_description.html', comic=comic)
        else:
            if not current_user.is_anonymous:
                uid = session.get('user_id')
                cid = comic.id
                chapter = chapter
                type = '1'
                history = History.query.filter_by(uid=uid).filter_by(cid=cid).first()
                if history:
                    history.chapter = chapter
                    history.updatetime = datetime.now().strftime('%Y%m%d%H%M%S')
                else:
                    history = History()
                    history.uid = uid
                    history.cid = cid
                    history.chapter = chapter
                    history.type = type
                    history.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
                    history.updatetime = datetime.now().strftime('%Y%m%d%H%M%S')
                db.session.add(history)
                db.session.commit()

            filelist = myftp.listfiles('/comics' + '/' + id + '/' + chapter)
            filelist = ['/comics' + '/' + id + '/' + chapter + '/' + str(i + 1) + '.jpg' for i in range(len(filelist))]
            return render_template('cartoon_browse.html', imglist=filelist, cur=chapter, len=comic.curchapter)


@main.route('/reading', methods=['GET'])
def reading():
    packages = Package.query.filter_by(type=4).all()
    print packages
    return render_template('reading.html', packages=packages)


@main.route('/reading/<bookid>', methods=['GET'])
def readinginfo(bookid):
    chapters = Chapter.query.filter_by(bookid=bookid).order_by(Chapter.chapterid).all()
    reading = Reading.query.filter_by(bookid=bookid).first()
    chapter = request.args.get('chapter')
    if request.args.get('type') == 'json':
        if session.get(reading.packageid) or int(chapter) <= reading.freechapter + 1:
            return 'success'
        else:
            return 'noauthority'
    else:
        if chapter:
            chapter = chapters[int(chapter) - 1]
            chaptername = chapter.chaptername.split(' ')
            if len(chaptername) > 1:
                chaptername = chapter.chaptername[3:]
            else:
                chaptername = chaptername[0][:2]
            ptaglist = re.findall(u'\<p\>[\s　]*(.*?)\<\/p\>', chapter.content)
            return render_template('read_browse.html', ptaglist=ptaglist, name=chaptername, cur=chapter,
                                   len=len(chapters))
        else:
            chapter_dict_list = []
            for c in chapters:
                chaptername = c.chaptername.split(' ')
                print chaptername
                dict = {}
                dict['a'] = chaptername[0].split('-')[1]
                dict['b'] = chaptername[1] if len(chaptername) > 1 else u'前言'
                dict['id'] = c.chapterid
                chapter_dict_list.append(dict)
            return render_template('read_description.html', book=reading, chapters=chapter_dict_list, flag=True)


@main.route('/my', methods=['GET'])
def my():
    if not current_user.is_anonymous:
        return render_template('my_loggedin.html')
    else:
        return render_template('my.html')


@main.route('/index', methods=['GET'])
def index():
    return redirect(url_for('main.comic'))
