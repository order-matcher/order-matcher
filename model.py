import datetime

from database import get

db = get()

class Consumer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    bin = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    adress = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String, db.ForeignKey('category.name'),
        nullable=False)
    order = db.relationship('Order', backref='orders') 

class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    bin = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    adress = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String, db.ForeignKey('category.name'),
        nullable=False)
    offers = db.relationship('Offer', backref='offers') 


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    categories_1 = db.relationship('Consumer', backref='consumers')
    categories_2 = db.relationship('Provider', backref='providers')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_start = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_end = db.Column(db.DateTime)
    contact_person = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    costs = db.Column(db.Float, primary_key=True)
    currency = db.Column(db.String(100), nullable=False)
    consumer = db.Column(db.String, db.ForeignKey('consumer.name'),
        nullable=False)

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_offer =  db.Column(db.DateTime, default=datetime.datetime.utcnow)
    offered_price = db.Column(db.Float, primary_key=True)
    currency = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.Text, nullable=False)
    provider = db.Column(db.String, db.ForeignKey('provider.name'),
        nullable=False)