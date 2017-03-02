from . import main
from flask import render_template
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

@main.route('/',methods=['GET', 'POST'])
def index():
    print request.method
    form = GameForm()
    if request.method == 'POST':
        game = Game()
        myftp = MyFTP(config.FTP_ADDR,config.FTP_PORT,config.FTP_USER,config.FTP_PWD, '/')
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
            myftp.uploadFiles('/res/games/', os.path.join('./res/', filename))
            game.img_icon = prefix + 'games/' + filename
        if form.data['type'] == '1':
            file = request.files['apk']
            if file:
                filename = secure_filename(file.filename)
                filename = generate_name(filename)
                print filename
                file.save(os.path.join('./res/', filename))
                myftp.uploadFiles('/res/games/', os.path.join('./res/', filename))
                game.url = prefix + 'games/' + filename
            for index,filename in enumerate(request.files.getlist('screenshot')):
                filename = generate_name(secure_filename(file.filename))
                print filename
                file.save(os.path.join('./res/', filename))
                myftp.uploadFiles('/res/games/', os.path.join('./res/', filename))
                setattr(game, 'img_screenshot_'+str(index+1), prefix + 'games/' + filename)
        game.createtime = datetime.now().strftime('%Y%m%d%H%M%S')
        db.session.add(game)
        db.session.commit()
        print game.to_json()
    return render_template('admin.html', form=form)