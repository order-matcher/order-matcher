from flask_sqlalchemy import SQLAlchemy


def init(app):
    global db
    db = SQLAlchemy(app)


def get():
    return db