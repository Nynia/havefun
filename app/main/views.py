from . import main
from flask import render_template,session
from .forms import GameForm
from flask import request
from app.api_1_0.game import Game
from werkzeug.utils import secure_filename
import os
from app.utils.ftp import MyFTP
from app.utils.func import generate_name
import config
from app import db
from datetime import datetime
from flask_login import current_user
from app.models import Package,OrderRelation,Comic

@main.route('/',methods=['GET', 'POST'])
def index():
    print request.method
    form = GameForm()
    if request.method == 'POST':
        game = Game()
        myftp = MyFTP(config.FTP_ADDR,config.FTP_PORT,config.FTP_USER,config.FTP_PWD, '/')
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
            for index,file in enumerate(request.files.getlist('screenshot')):
                filename = generate_name(secure_filename(file.filename))
                print filename
                file.save(os.path.join('./res/', filename))
                myftp.uploadFiles(os.path.join('./res/', filename), '/games/jpg/')
                setattr(game, 'img_screenshot_'+str(index+1), prefix + 'games/' + filename)
        game.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
        db.session.add(game)
        db.session.commit()
        print game.to_json()
    return render_template('admin.html', form=form)

@main.route('/game',methods=['GET'])
def game():
    packages = Package.query.filter_by(type=2).all()
    h5 = Game.query.filter_by(type=2).limit(4).all()
    print h5
    return  render_template('game.html',packages=packages,h5=h5)

@main.route('/package',methods=['GET'])
def package():
    id = request.args.get('id')
    package = Package.query.get(int(id))
    ordered = False
    if not current_user.is_anonymous:
        if package.productid in session['ordered']:
            ordered = True
    if package.type == '1':
        #comic
        comics = Comic.query.filter_by(packageid=id).all()
        return render_template('package_comic.html', package=package, comics=comics, flag=ordered)
    elif package.type == '2':
        #game
        games = Game.query.filter_by(packageid=id).all()
        return render_template('package_game.html', package=package, games=games, flag=ordered)
    elif package.type == '3':
        #music
        pass
    else:
        #reading
        pass

@main.route('/gamedetail',methods=['GET'])
def gamedetail():
    id = request.args.get('id')
    game = Game.query.get(int(id))
    return render_template('game_detail.html',game=game)

@main.route('/comic',methods=['GET'])
def comic():
    packages = Package.query.filter_by(type=1).all()
    print packages
    return render_template('cartoon.html',packages=packages)

@main.route('/comicdescription',methods=['GET'])
def comicdetail():
    id = request.args.get('id')
    comic = Comic.query.get(int(id))
    return render_template('cartoon_description.html',comic=comic)

@main.route('/comicbrowse/<id>',methods=['GET'])
def comicbrowse(id):
    chapter = request.args.get('chapter')
    myftp = MyFTP(config.FTP_ADDR, config.FTP_PORT, config.FTP_USER, config.FTP_PWD, '/')
    myftp.login()
    filelist = myftp.listfiles('/comics'+'/'+id+'/'+chapter)
    filelist = ['/comics'+'/'+id+'/'+chapter+'/'+str(i+1)+'.jpg' for i in range(len(filelist))]
    print filelist
    return render_template('cartoon_browse.html',imglist=filelist)

