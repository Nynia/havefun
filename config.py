import os
basedir = os.path.abspath(os.path.dirname(__file__))

# qiniu
QINIU_ACCESS_KEY = 'jJnJu4_d7YH8hhhB-J4J8Jr537T_-yk9BIsin75M'
QINIU_SECRET_KEY = 'WpidgDmScl866DLV22LT2Qon19oDkiLmRbxhDrGq'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'skks'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #task
    JOBS = [
        {
            'id': 'job1',
            'func': 'app.tasks:job1',
            'args': (1, 2),
            'trigger': 'cron',
            'hour': '17',
            'minute': '23',
            'second': '1'
        }
    ]
    SCHEDULER_API_ENABLED = True

    @staticmethod
    def init_app(app):
        pass

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@127.0.0.1/havefun'

class ProductionConfig(Config):
    pass

config = {
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default':TestingConfig,
}
