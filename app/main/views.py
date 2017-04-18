# -*-coding=utf-8-*-
from . import main
from flask import render_template, session, redirect, url_for, jsonify
from .forms import GameForm
from flask import request
from app.api_1_0.game import Game
from werkzeug.utils import secure_filename
import os, re, requests, json, hashlib,random
from app.utils.ftp import MyFTP
from app.utils.func import generate_name
import config
from app import db
from datetime import datetime
from flask_login import current_user
from app.models import Package, Comic, Reading, Chapter, History, OrderRelation, OrderHistroy,ComicChapterInfo


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
    h5 = Game.query.filter_by(type=2).limit(7).all()
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
    return render_template('game_description.html', game=game, flag=flag, package=package)


@main.route('/comic', methods=['GET'])
def comic():
    packages = Package.query.filter_by(type=1).all()
    print packages
    return render_template('cartoon.html', packages=packages)


@main.route('/comic/<id>', methods=['GET'])
def comicbrowse(id):
    comic = Comic.query.get(int(id))
    chapter = request.args.get('chapter')
    package = Package.query.get(comic.packageid)
    if request.args.get('type') == 'json':
        if session.get(comic.packageid) or int(chapter) <= comic.freechapter:
            return jsonify({
                'code': '0',
                'msg': chapter
            })
        else:
            return jsonify({
                'code': '1',
                'msg': chapter
            })
    else:
        if chapter == None:
            return render_template('cartoon_description.html', comic=comic, package=package)
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

            chapterinfo = ComicChapterInfo.query.filter_by(bookid=id).filter_by(chapterid=chapter).first()
            filelist2 = []
            for i in range(chapterinfo.quantity):
                if i < 10:
                    filelist2.append('/comics' + '/' + id + '/' + chapter + '/' + '0' + str(i + 1) + '.jpg')
                else:
                    filelist2.append('/comics' + '/' + id + '/' + chapter + '/' + str(i + 1) + '.jpg')
            print filelist2
            return render_template('cartoon_browse.html', imglist=filelist2, cur=chapter, len=comic.curchapter,
                                   package=package)


@main.route('/reading', methods=['GET'])
def reading():
    packages = Package.query.filter_by(type=4).all()
    print packages
    readings = Reading.query.all()
    random.shuffle(readings)
    return render_template('reading.html', packages=packages,books=readings)


@main.route('/reading/<bookid>', methods=['GET'])
def readinginfo(bookid):
    chapters = Chapter.query.filter_by(bookid=bookid).order_by(Chapter.chapterid).all()
    reading = Reading.query.filter_by(bookid=bookid).first()
    chapter = request.args.get('chapter')
    package = Package.query.get(reading.packageid)
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
                                   len=len(chapters), package=package)
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
            return render_template('read_description.html', book=reading, chapters=chapter_dict_list, flag=True,
                                   package=package)


@main.route('/my', methods=['GET'])
def my():
    if not current_user.is_anonymous:
        return render_template('my_loggedin.html')
    else:
        return render_template('my.html')


@main.route('/index', methods=['GET'])
def index():
    return redirect(url_for('main.comic'))

@main.route('/', methods=['GET'])
def root():
    return redirect(url_for('main.comic'))


@main.route('/subscribe', methods=['POST'])
def subscribe():
    productid = request.form.get('productid')
    phonenum = request.form.get('phonenum')
    package = Package.query.get(productid)
    chargeid = package.chargeid
    secret = package.secret
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    token = hashlib.sha1(chargeid + timestamp + secret).hexdigest()
    data = {
        'action': 'subscribe',
        'spId': package.spid,
        'chargeId': package.chargeid,
        'phoneNum': phonenum,
        'orderType': '1',
        'timestamp': timestamp,
        'accessToken': token
    }
    r = requests.post('http://61.160.185.51:9250/ismp/serviceOrder', data=data)
    json_result = json.loads(r.text)
    print json_result
    err_code = json_result['errcode']
    err_msg = json_result['errmsg']
    if err_code == '0':
        orderaction = OrderRelation.query.filter_by(phonenum=phonenum).filter_by(productid=productid).first()
        if not orderaction:
            orderaction = OrderRelation()
        orderhistory = OrderHistroy()
        orderaction.productid = productid
        orderaction.phonenum = phonenum
        orderhistory.productid = productid
        orderhistory.phonenum = phonenum
        orderaction.ordertime = timestamp
        orderaction.status = '1'

        orderhistory.action = '1'
        orderhistory.createtime = timestamp

        db.session.add(orderaction)
        db.session.add(orderhistory)
        db.session.commit()

        session[productid] = 1

        return jsonify({
            'code': err_code,
            'message': err_msg,
            'data': None
        })

    else:
        return jsonify({
            'code': err_code,
            'message': err_msg,
            'data': None
        })

@main.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    productid = request.form.get('productid')
    phonenum = request.form.get('phonenum')
    package = Package.query.get(productid)
    chargeid = package.chargeid
    secret = package.secret
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    token = hashlib.sha1(chargeid + timestamp + secret).hexdigest()
    data = {
        'action': 'unsubscribe',
        'spId': package.spid,
        'chargeId': package.chargeid,
        'phoneNum': phonenum,
        'orderType': '1',
        'timestamp': timestamp,
        'accessToken': token
    }
    r = requests.post('http://61.160.185.51:9250/ismp/serviceOrder', data=data)
    json_result = json.loads(r.text)
    print json_result
    err_code = json_result['errcode']
    err_msg = json_result['errmsg']
    if err_code == '0':
        orderaction = OrderRelation.query.filter_by(phonenum=phonenum).filter_by(productid=productid).first()
        if not orderaction:
            orderaction = OrderRelation()
        orderhistory = OrderHistroy()
        orderaction.productid = productid
        orderaction.phonenum = phonenum
        orderhistory.productid = productid
        orderhistory.phonenum = phonenum

        orderaction.canceltime = timestamp
        orderaction.status = '4'
        orderhistory.action = '0'
        orderhistory.createtime = timestamp

        db.session.add(orderaction)
        db.session.add(orderhistory)
        db.session.commit()

        session.pop(productid)

        return jsonify({
            'code': err_code,
            'message': err_msg,
            'data': None
        })

    else:
        return jsonify({
            'code': err_code,
            'message': err_msg,
            'data': None
        })


@main.route('/video', methods=['GET'])
def vedio():
    return render_template('video.html')

@main.route('/music', methods=['GET'])
def music():
    return render_template('music.html')

@main.route('/myorder', methods=['GET'])
def myorder():
    phonenum = session.get('phonenum')
    data = []
    relation = OrderRelation.query.filter_by(phonenum=phonenum).filter_by(status='1').all()
    for r in relation:
        package = Package.query.get(r.productid)
        dict = {}
        dict['productname'] = package.productname
        t = r.ordertime
        dict['timestamp'] = t[:4]+'-'+t[4:6]+'-'+t[6:8]+' '+t[8:10]+':'+t[10:12]+':'+t[12:14]
        dict['productid'] = package.productid
        data.append(dict)
    return render_template('myorder.html', data=data)
