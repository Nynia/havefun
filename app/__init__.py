from flask import Flask
from flask_apscheduler import APScheduler
from flask_bootstrap import Bootstrap
from config import config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap=Bootstrap(app)
db = SQLAlchemy(app)

app.config.from_object(config['testing'])

#scheduler = APScheduler()
#scheduler.init_app(app)
#scheduler.start()

import views,api_1_0.package,api_1_0.comic,api_1_0.user