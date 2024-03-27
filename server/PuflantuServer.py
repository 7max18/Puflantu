import os 
from app import create_app, db, config
import pymysql
import pandas as pd
import click

pymysql.install_as_MySQLdb()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    