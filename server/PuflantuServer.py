import os 
from app import create_app, db
import pymysql
from flask_migrate import Migrate

pymysql.install_as_MySQLdb()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)