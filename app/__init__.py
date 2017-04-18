from flask import Flask
from flask_apscheduler import APScheduler
from flask_bootstrap import Bootstrap
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import requests
from app.utils.ftp import MyFTP

bootstrap = Bootstrap()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'normal'
login_manager.login_view = 'auth.login'

#scheduler = APScheduler()

#myftp = MyFTP('192.168.114.138', 12345, 'jsgx', 'jsgx2017', '/')

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    #scheduler.init_app(app)
    #scheduler.start()

    #myftp.login()

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

def get_readings_session():
    url = 'http://wap.tyread.com/user/registAndLogin.action?is_ctwap=0'
    s = requests.Session()
    data = {
        'phoneNum_input': '18118999630',
        'randomCode': '147976',
        'pic_code': 'bgbg',
        'autoLogin': '1',
        'from': 'login',
    }
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    }
    _cookies = {
        'JSESSIONID': 'C9E5BBC28106F2AEC0B67F4988C6BFFF'
    }
    r = s.post(url, headers=headers, data=data, cookies=_cookies)
    r.encoding = 'utf-8'
    print r.text
    return s

#reading_session = get_readings_session()