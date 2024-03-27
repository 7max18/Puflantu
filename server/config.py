import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'f216029a49d039ff1207c39658af1228'
    SQLALCHEMY_DATABASE_URI = 'mariadb://root:mysqlpassword@localhost/Puflantu'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_KEY = 'edc93c55c9afc5536c9a32aa4d230594'
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}