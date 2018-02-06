# -*-coding=utf-8-*-
from . import main
from flask import render_template, session, redirect, url_for, jsonify
from .forms import GameForm
from flask import request
from app.api_1_0.game import Game
from werkzeug.utils import secure_filename
import os, re, random
from app.utils.ftp import MyFTP
from app.utils.func import generate_name
from app import db
from datetime import datetime
from flask_login import current_user
from app.models import Package, Comic, Reading, Chapter, ViewRecord, OrderRelation, AccessLog, ComicChapterInfo, \
    FavorInfo, IntegralRecord, IntegralStrategy, User, RecommendH5, RecommendComic


@main.route('/xss', methods=['GET'])
def getcookie():
    msg = request.args.get('msg')
    print 'cookie:' + msg
    return datetime.now().strftime('%Y%m%d')


@main.route('/config', methods=['GET', 'POST'])
def config():
    print request.method
    form = GameForm()
    if request.method == 'POST':
        game = Game()
        myftp = MyFTP('192.168.114.138', 12345, 'jsgx', 'jsgx2017', '/')
        myftp.login()
        prefix = 'http://221.228.17.87/res/'
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
    return redirect(url_for('main.game_2'))


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


@main.route('/index_1', methods=['GET'])
def game_1():
    # packages = Package.query.filter_by(type=2).all()
    h5 = RecommendH5.query.all()
    # return render_template('game.html', packages=packages, h5=h5)
    return render_template('v1_1/index-1.html', h5=h5)


@main.route('/index_2', methods=['GET'])
def game_2():
    packages = Package.query.filter_by(type=2).all()
    h5 = RecommendH5.query.all()
    # return render_template('game.html', packages=packages, h5=h5)
    return render_template('v1_1/index-2.html', packages=packages, h5=h5)


@main.route('/index_3', methods=['GET'])
def game_3():
    return render_template('v1_1/index-3.html')


@main.route('/h5game', methods=['GET'])
def h5game():
    id = request.args.get('id')
    game = Game.query.get(int(id))
    integral = 0
    if not current_user.is_anonymous:
        uid = session.get('user_id')
        today = datetime.now().strftime('%Y%m%d')
        user = User.query.get(int(uid))
        # 添加积分记录
        viewrecords = ViewRecord.query.filter_by(user_id=uid).filter_by(target_type='2').filter_by(target_id=id).filter(
            ViewRecord.createtime.startswith(today)).all()
        if not viewrecords:
            integral_strategy = IntegralStrategy.query.filter_by(description=u'玩H5游戏').first()
            integral_history = IntegralRecord.query.filter_by(uid=uid).filter_by(action=integral_strategy.id).filter(
                IntegralRecord.timestamp.startswith(today)).all()
            history_integral_today = 0
            if integral_history:
                history_integral_today = reduce(lambda x, y: x + y, [r.change for r in integral_history])
                print history_integral_today
            # 当日游戏积分未超过80
            if history_integral_today < 80:
                integral = integral_strategy.value
                user.integral = user.integral + integral_strategy.value
                db.session.add(user)

                integral_record = IntegralRecord()
                integral_record.uid = uid
                integral_record.action = integral_strategy.id
                integral_record.change = integral_strategy.value
                integral_record.timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

                db.session.add(integral_record)
        # 添加访问记录
        viewrecord = ViewRecord()
        viewrecord.target_type = '2'
        viewrecord.user_id = uid
        viewrecord.target_id = id
        viewrecord.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
        db.session.add(viewrecord)
        db.session.commit()
    return render_template('game_h5.html', url=game.url, integral=integral)


@main.route('/game/<id>', methods=['GET'])
def gamedetail(id):
    game = Game.query.get(int(id))
    package = Package.query.get(game.packageid)
    flag = False
    # if session.get(package.productid):
    #     flag = True
    return render_template('game_description.html', game=game, flag=flag, package=package)


@main.route('/game/download', methods=['GET'])
def downloadgame():
    id = request.args.get('id')
    game = Game.query.get(int(id))
    if game:
        uid = session.get('user_id')
        today = datetime.now().strftime('%Y%m%d')
        user = User.query.get(int(uid))
        integral = 0
        # 添加积分记录
        integral_strategy = IntegralStrategy.query.filter_by(description=u'下载游戏').first()
        integral_history = IntegralRecord.query.filter_by(uid=uid).filter_by(action=integral_strategy.id).filter(
            IntegralRecord.timestamp.startswith(today)).all()
        history_integral_today = 0
        if integral_history:
            history_integral_today = reduce(lambda x, y: x + y, [r.change for r in integral_history])
            print history_integral_today
        # 当日游戏积分未超过80
        if history_integral_today < 80:
            integral = integral_strategy.value
            user.integral = user.integral + integral_strategy.value
            db.session.add(user)

            integral_record = IntegralRecord()
            integral_record.uid = uid
            integral_record.action = integral_strategy.id
            integral_record.change = integral_strategy.value
            integral_record.timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

            db.session.add(integral_record)
        return jsonify({
            'code': '0',
            'integral': integral,
            'next': game.url
        })
    else:
        return jsonify({
            'code': '109',
            'msg': 'game not exist'
        })


@main.route('/comic', methods=['GET'])
def comic():
    packages = Package.query.filter_by(type=1).all()
    recommends = RecommendComic.query.all()
    return render_template('cartoon.html', packages=packages, recommends=recommends)


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
            favor = None
            if not current_user.is_anonymous:
                uid = session.get('user_id')
                cid = comic.id
                favorinfo = FavorInfo.query.filter_by(uid=uid).filter_by(type='1').filter_by(cid=cid).first()
                favor = True if favorinfo and favorinfo.state == '1' else False
                print 'favor:' + str(favor)
            return render_template('cartoon_description.html', comic=comic, package=package,
                                   recentchapter=None, favor=favor)
        else:
            if not current_user.is_anonymous:
                uid = session.get('user_id')
                user = User.query.get(int(uid))
                cid = comic.id
                chapter = chapter
                type = '1'
                today = datetime.now().strftime('%Y%m%d')
                viewrecord = ViewRecord.query.filter_by(user_id=uid).filter_by(target_type='1').filter_by(
                    target_id=cid).first()
                if not viewrecord:
                    viewrecord = ViewRecord()
                    viewrecord.user_id = uid
                    viewrecord.target_id = cid
                    viewrecord.target_chapter = chapter
                    viewrecord.target_type = type
                    viewrecord.createtime = datetime.now().strftime('%Y%m%d%H%M%S')

                    # integral
                    integral_strategy = IntegralStrategy.query.filter_by(description=u'看动漫').first()
                    integral_history = IntegralRecord.query.filter_by(uid=uid).filter_by(
                        action=integral_strategy.id).filter(
                        IntegralRecord.timestamp.startswith(today)).all()
                    history_integral_today = 0
                    if integral_history:
                        history_integral_today = reduce(lambda x, y: x + y, [r.change for r in integral_history])
                        print history_integral_today
                    if history_integral_today < 80:
                        integral = integral_strategy.value
                        user.integral = user.integral + integral_strategy.value
                        db.session.add(user)

                        integral_record = IntegralRecord()
                        integral_record.uid = uid
                        integral_record.action = integral_strategy.id
                        integral_record.change = integral_strategy.value
                        integral_record.timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                        db.session.add(integral_record)
                else:
                    viewrecord.target_chapter = chapter
                    viewrecord.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
                db.session.add(viewrecord)
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
                                   package=package, integral=integral)


@main.route('/reading', methods=['GET'])
def reading():
    packages = Package.query.filter_by(type=4).all()
    print packages
    readings = Reading.query.all()
    random.shuffle(readings)
    return render_template('reading.html', packages=packages, books=readings)


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
    print session
    print current_user
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

        ##
        uid = session.get('user_id')
        records = []
        comic_record = db.session.execute(
            ('select A.id,A.comicname,A.banner,A.curchapter,B.target_chapter,B.createtime '
             'from comic as A,(select * from view_record where id in (select max(id) id '
             'from view_record where target_type=\'1\' and user_id=%s '
             'group by target_id)) as B where A.id=B.target_id;') % uid)
        game_record = db.session.execute(('select A.id,A.name,A.img_icon,A.url,B.createtime '
                                          'from game as A,(select * from view_record where id in (select max(id) id '
                                          'from view_record where target_type=\'2\' and user_id=%s '
                                          'group by target_id)) as B where A.id=B.target_id order by createtime desc;') % uid)
        for item in comic_record.fetchall():
            records.append(
                {
                    'id': item[0],
                    'name': item[1],
                    'type': '1',
                    'banner': item[2],
                    'chapter': item[4],
                    'updatetime': item[5],
                    'progress': int(item[4] * 1.0 / item[3] * 100)
                }
            )
        for item in game_record:
            records.append(
                {
                    'id': item[0],
                    'name': item[1],
                    'type': '2',
                    'banner': item[2],
                    'url': item[3],
                    'updatetime': item[4]
                }
            )
        print records
        # history
        # view_records = ViewRecord.query.filter_by(user_id=current_user.id).all()
        # comic_game_records = []
        # for item in view_records:
        #     if item.target_type == '1':
        #         comic_item = Comic.query.get(int(item.target_id))
        #         comic_game_records.append(
        #             {
        #                 'id': comic_item.id,
        #                 'name': comic_item.comicname,
        #                 'type': '1',
        #                 'banner': comic_item.banner,
        #                 'updatetime': item.createtime,
        #                 'chapter': item.target_chapter,
        #                 'progress': int(item.target_chapter * 1.0 / comic_item.curchapter * 100)
        #             })
        #     elif item.target_type == '2':
        #         # game
        #         game_item = Game.query.get(int(item.target_id))
        #         comic_game_records.append(
        #             {
        #                 'id': game_item.id,
        #                 'name': game_item.name,
        #                 'type': '2',
        #                 'banner': game_item.img_icon,
        #                 'updatetime': item.createtime,
        #                 'url': game_item.url
        #             })

        # integral
        integral = current_user.integral
        if integral < 400:
            level = 1
        elif integral < 600:
            level = 2
        elif integral < 1000:
            level = 3
        elif integral < 1600:
            level = 4
        elif integral < 2400:
            level = 5
        elif integral < 3400:
            level = 6
        elif integral < 3600:
            level = 7
        elif integral < 5000:
            level = 8
        elif integral < 6600:
            level = 9
        else:
            level = 10
        return render_template('v1_1/my_logged.html', checkinstatus=checkinstatus, checkindays=checkindays,
                               records=sorted(records, reverse=True, key=lambda x:x['updatetime']), level=level)
    else:
        return render_template('v1_1/my.html')


@main.route('/myorder', methods=['GET'])
def myorder():
    data = []
    if not current_user.is_anonymous:
        phonenum = session.get('phonenum')
        relation = OrderRelation.query.filter_by(phonenum=phonenum).filter_by(status='1').all()
        for r in relation:
            package = Package.query.get(r.productid)
            dict = {}
            dict['productname'] = package.productname
            t = r.ordertime
            dict['timestamp'] = t[:4] + '-' + t[4:6] + '-' + t[6:8] + ' ' + t[8:10] + ':' + t[10:12] + ':' + t[12:14]
            dict['productid'] = package.productid
            data.append(dict)
        print data
        return render_template('myorder.html', data=data)
    else:
        return render_template("notlogged.html", title=u"我的订购")


@main.route('/collection', methods=['GET'])
def mycollection():
    data = []
    if not current_user.is_anonymous:
        uid = current_user.id
        faverinfos = FavorInfo.query.filter_by(uid=uid).filter_by(state='1').all()
        # 默认只有动漫 -type=1
        for f in faverinfos:
            cid = f.cid
            viewrecord = ViewRecord.query.filter_by(user_id=uid).filter_by(target_id=cid).filter_by(
                target_type='1').first()
            if viewrecord:
                recentchap = viewrecord.target_chapter
            else:
                recentchap = 1
            data.append({
                'type': '1',
                'id': cid,
                'name': f.name,
                'img': f.img,
                'recentchap': recentchap
            })
        return render_template('collection.html', data=data)

    else:
        return render_template("notlogged.html", title=u"我的收藏")


@main.route('/mall', methods=['GET'])
def mall():
    if not current_user.is_anonymous:
        return render_template('mall.html')
    else:
        return render_template("notlogged.html", title=u"商城")


@main.route('/mysign', methods=['GET'])
def sign():
    if not current_user.is_anonymous:
        return render_template('sign.html')
    else:
        return render_template("notlogged.html", title=u"我的签到")


@main.route('/flow', methods=['GET'])
def flow():
    if current_user.is_anonymous:
        return redirect('http://flow.jsinfo.net')
    else:
        phonenum = current_user.phonenum
        from app.utils.func import AES_encrypt
        encrptyed = AES_encrypt(phonenum)
        url = 'http://flow.jsinfo.net?phone=%s' % encrptyed
        print url
        return redirect(url)


@main.route('/history', methods=['GET'])
def history():
    today = []
    earlier = []
    if not current_user.is_anonymous:
        uid = session.get('user_id')
        comic_record = db.session.execute(('select A.id,A.comicname,A.banner,B.target_chapter,B.createtime '
                                           'from comic as A,(select * from view_record where id in (select max(id) id '
                                           'from view_record where target_type=\'1\' and user_id=%s '
                                           'group by target_id)) as B where A.id=B.target_id;') % uid)
        for item in comic_record.fetchall():
            if item[-1].startswith(datetime.now().strftime('%Y%m%d')):
                today.append({
                    'id': item[0],
                    'name': item[1],
                    'banner': item[2],
                    'chapter': item[3],
                    'createtime': item[4]
                })
            else:
                earlier.append({
                    'id': item[0],
                    'name': item[1],
                    'banner': item[2],
                    'chapter': item[3],
                    'createtime': item[4]
                })
    else:
        return render_template("notlogged.html", title=u"观看历史")
    return render_template('history.html', today=today, earlier=earlier)


@main.route('/find', methods=['GET'])
def discovery():
    return render_template('v1_1/find.html')


@main.route('/weal', methods=['GET'])
def weal():
    return render_template('v1_1/weal.html')


@main.route('/follow', methods=['GET'])
def follow():
    data = []
    if not current_user.is_anonymous:
        uid = current_user.id
        faverinfos = FavorInfo.query.filter_by(uid=uid).filter_by(state='1').all()
        # 默认只有动漫 -type=1
        for f in faverinfos:
            cid = f.cid
            viewrecord = ViewRecord.query.filter_by(user_id=uid).filter_by(target_id=cid).filter_by(
                target_type='1').first()
            if viewrecord:
                recentchap = viewrecord.target_chapter
            else:
                recentchap = 1
            data.append({
                'type': '1',
                'id': cid,
                'name': f.name,
                'img': f.img,
                'recentchap': recentchap
            })
        return render_template('follow.html', data=data)

    else:
        return render_template("notlogged.html", title=u"我的收藏")


@main.route('/download', methods=['GET'])
def downloadpage():
    return render_template('download.html')


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
        # 处理登录用户的积分

    db.session.add(accesslog)
    db.session.commit()

    return response
