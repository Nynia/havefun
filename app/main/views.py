# -*-coding=utf-8-*-
from . import main
from flask import render_template, session, redirect, url_for, jsonify
from .forms import GameForm
from flask import request
from app.api_1_0.game import Game
from werkzeug.utils import secure_filename
import os,re,random
from app.utils.ftp import MyFTP
from app.utils.func import generate_name
import config
from app import db
from datetime import datetime
from flask_login import current_user
from app.models import Package, Comic, Reading, Chapter, ViewInfo, OrderRelation,AccessLog,ComicChapterInfo,FavorInfo,IntegralRecord,IntegralStrategy,User

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

@main.route('/', methods=['GET'])
def root():
    return redirect(url_for('main.comic'))

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


@main.route('/game', methods=['GET'])
def game():
    packages = Package.query.filter_by(type=2).all()
    h5 = Game.query.filter_by(type=2).limit(11).all()
    print h5
    return render_template('game.html', packages=packages, h5=h5)

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
    integral = 0
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
            if not current_user.is_anonymous:
                uid = session.get('user_id')
                cid = comic.id
                favorinfo = FavorInfo.query.filter_by(uid=uid).filter_by(type='1').filter_by(cid=cid).first()
                favor = True if favorinfo and favorinfo.state=='1' else False
                print 'favor:' + str(favor)
                viewinfo = ViewInfo.query.filter_by(userid=uid).filter_by(comicid=cid).first()
                if viewinfo:
                    recentchapter = viewinfo.recentchapter
                    return render_template('cartoon_description.html', comic=comic, package=package, recentchapter=recentchapter,favor=favor)
                else:
                    return render_template('cartoon_description.html', comic=comic, package=package,
                                           recentchapter=None,favor=favor)
            else:
                return render_template('cartoon_description.html', comic=comic, package=package,
                                       recentchapter=None)
        else:
            if not current_user.is_anonymous:
                uid = session.get('user_id')
                cid = comic.id
                chapter = chapter
                type = '1'

                viewinfo = ViewInfo.query.filter_by(userid=uid).filter_by(comicid=cid).first()
                today = datetime.now().strftime('%Y%m%d')
                if viewinfo:
                    #integral
                    lastviewtime = viewinfo.updatetime
                    if not lastviewtime.startswith(today):
                        integral_strategy = IntegralStrategy.query.filter_by(description=u'看动漫').first()

                        user = User.query.get(int(uid))

                        integral_history = IntegralRecord.query.filter_by(action=integral_strategy.id).filter(IntegralRecord.timestamp.startswith(today)).all()
                        history_integral_today = 0
                        if integral_history:
                            history_integory_today = reduce(lambda x, y: x + y, [r.change for r in integral_history])
                            print history_integory_today
                        if history_integral_today < 80:
                            print history_integory_today
                            integral = integral_strategy.value
                            user.integral = user.integral + integral_strategy.value
                            db.session.add(user)

                            integral_record = IntegralRecord()
                            integral_record.uid = uid
                            integral_record.action = integral_strategy.id
                            integral_record.change = integral_strategy.value
                            integral_record.timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

                            db.session.add(integral_record)
                    viewinfo.recentchapter = chapter
                    viewinfo.updatetime = datetime.now().strftime('%Y%m%d%H%M%S')

                else:
                    #integral
                    integral_strategy = IntegralStrategy.query.filter_by(description=u'看动漫').first()

                    user = User.query.get(int(uid))

                    integral_history = IntegralRecord.query.filter(IntegralRecord.timestamp.startswith(today)).filter_by(
                        action=integral_strategy.id).all()
                    history_integral_today = 0
                    if integral_history:
                        history_integory_today = reduce(lambda x, y: x + y, [r.change for r in integral_history])
                        print history_integory_today
                    if history_integral_today < 80:
                        print history_integory_today
                        integral = integral_strategy.value
                        user.integral = user.integral + integral_strategy.value
                        db.session.add(user)

                        integral_record = IntegralRecord()
                        integral_record.uid = uid
                        integral_record.action = integral_strategy.id
                        integral_record.change = integral_strategy.value
                        integral_record.timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

                        db.session.add(integral_record)
                    viewinfo = ViewInfo()
                    viewinfo.userid = uid
                    viewinfo.comicid = cid
                    viewinfo.recentchapter = chapter
                    viewinfo.type = type
                    viewinfo.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
                    viewinfo.updatetime = datetime.now().strftime('%Y%m%d%H%M%S')

                db.session.add(viewinfo)
                db.session.commit()

            chapterinfo = ComicChapterInfo.query.filter_by(bookid=id).filter_by(chapterid=chapter).first()
            filelist2 = []
            for i in range(chapterinfo.quantity):
                if i < 9:
                    filelist2.append('/comics' + '/' + id + '/' + chapter + '/' + '0' + str(i + 1) + '.jpg')
                else:
                    filelist2.append('/comics' + '/' + id + '/' + chapter + '/' + str(i + 1) + '.jpg')
            print filelist2
            return render_template('cartoon_browse.html', imglist=filelist2, cur=chapter, len=comic.curchapter,
                                   package=package,integral=integral)

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

@main.route('/video', methods=['GET'])
def vedio():
    return render_template('video.html')

@main.route('/music', methods=['GET'])
def music():
    return render_template('music.html')

@main.route('/my', methods=['GET'])
def my():
    if not current_user.is_anonymous:
        import datetime
        yestoday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
        today = datetime.date.today().strftime('%Y%m%d')
        lastcheckin = current_user.lastcheckin
        if lastcheckin and (lastcheckin.startswith(yestoday) or lastcheckin.startswith(today)):
            checkindays = current_user.continus_checkin
        else:
            checkindays = 0
        if lastcheckin and lastcheckin.startswith(today):
            checkinstatus = True
        else:
            checkinstatus = False
        print checkinstatus
        return render_template('my_loggedin.html',checkinstatus=checkinstatus, checkindays=checkindays)
    else:
        return render_template('my.html')

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

@main.route('/mall', methods=['GET'])
def mall():
    return render_template('mall.html')

@main.route('/mysign', methods=['GET'])
def sign():

    return render_template('sign.html')

def _get_annymous_id():
    address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if address is not None:
        address = address.encode('utf-8').split(b',')[0].strip()
    user_agent = request.headers.get('User-Agent')
    if user_agent is not None:
        user_agent = user_agent.encode('utf-8')
    base = '{0}|{1}'.format(address, user_agent)
    import hashlib
    m2 = hashlib.md5()
    m2.update(base)
    return m2.hexdigest()[:16]

@main.after_request
def after_request(response):
    accesslog = AccessLog()
    accesslog.addr = request.url
    accesslog.remoteip = request.remote_addr
    accesslog.useragent = request.user_agent.string
    accesslog.timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    if current_user.is_anonymous:
        accesslog.uid = _get_annymous_id()
    else:
        accesslog.uid = current_user.id
        #处理登录用户的积分


    db.session.add(accesslog)
    db.session.commit()

    return response