from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Dictionary(db.Model):
    __tablename__ = "dictionary"

    id = db.Column(db.Integer , primary_key = True , nullable=False)
    puflantu = db.Column(db.String(64))
    english = db.Column(db.String(64))