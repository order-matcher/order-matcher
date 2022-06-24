from flask import Flask, jsonify, request
from schema import ConsumerSchema, ProviderSchema, OrderSchema, CategorySchema, OfferSchema
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound
from flask_sqlalchemy import SQLAlchemy
import datetime
# import sqlalchemy
# import json
# import jsonschema
import os


import database

    # with open("config.json") as config:
    #     config = json .load(config)

    # with open("config.schema.json") as schema:
    #     schema = json.load(schema)

    # try:
    #     jsonschema.validate(config, schema)
    # except jsonschema.ValidationError as error:
    #     print("schema validation failed: {}".format(error))
    #     exit(1)
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

    #database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.init(app)
db = database.get()
from model import *

# class Consumer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False, unique=True)
#     bin = db.Column(db.String, nullable=False, unique=True)
#     password = db.Column(db.String, nullable=False)
#     country = db.Column(db.String(100), nullable=False)
#     city = db.Column(db.String(100), nullable=False)
#     adress = db.Column(db.String(100), nullable=False)
#     category = db.Column(db.String, db.ForeignKey('category.name'),
#         nullable=False)
#     order = db.relationship('Order', backref='orders') 

# class Provider(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False, unique=True)
#     bin = db.Column(db.String, nullable=False, unique=True)
#     password = db.Column(db.String, nullable=False)
#     country = db.Column(db.String(100), nullable=False)
#     city = db.Column(db.String(100), nullable=False)
#     adress = db.Column(db.String(100), nullable=False)
#     category = db.Column(db.String, db.ForeignKey('category.name'),
#         nullable=False)
#     offers = db.relationship('Offer', backref='offers') 


# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     categories_1 = db.relationship('Consumer', backref='consumers')
#     categories_2 = db.relationship('Provider', backref='providers')

# class Order(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     date_start = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#     date_end = db.Column(db.DateTime)
#     contact_person = db.Column(db.Text, nullable=False)
#     phone = db.Column(db.Text, nullable=False)
#     costs = db.Column(db.Float, primary_key=True)
#     currency = db.Column(db.String(100), nullable=False)
#     consumer = db.Column(db.String, db.ForeignKey('consumer.name'),
#         nullable=False)

# class Offer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     date_offer =  db.Column(db.DateTime, default=datetime.datetime.utcnow)
#     offered_price = db.Column(db.Float, primary_key=True)
#     currency = db.Column(db.String(100), nullable=False)
#     contact_person = db.Column(db.Text, nullable=False)
#     provider = db.Column(db.String, db.ForeignKey('provider.name'),
#         nullable=False)

consumer_schema = ConsumerSchema()
consumers_schema = ConsumerSchema(many=True)

provider_schema = ProviderSchema()
providers_schema = ProviderSchema(many=True)

category_schema = CategorySchema()
categoris_schema = CategorySchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

offer_schema = OfferSchema()
offers_schema = OfferSchema(many=True)


def registered_handlers(app: Flask):
    @app.route("/categories/", methods=['GET'])
    def get_categories():
        all_categories = Category.query.all()
        return jsonify(categoris_schema.dump(all_categories))

    @app.route("/orders/", methods=['POST', 'GET', 'PUT', 'DELETE'])
    def orders():
        if request.method == 'GET':
            all_orders = Order.query.all()
            return jsonify(orders_schema.dump(all_orders))

    @app.route("/orders/add", methods=['POST'])
    def post_order():
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            data = order_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        try:
            consumer = Consumer.query.filter(Consumer.name == data['consumer']).one()
        except NoResultFound:
            return {"message": "This consumer does not exist."}, 400
        order = Order(**data)
        db.session.add(order)
        db.session.commit()
        result = order_schema.dump(Order.query.get(order.id))
        return {'massage':'Created new order', 'Order': result}

    @app.route("/consumers/", methods=['GET'])
    def get_consumers():
        all_consumers = Consumer.query.all()
        return jsonify(consumers_schema.dump(all_consumers))

    @app.route("/consumers/<int:pk>", methods=['GET'])
    def get_consumer(pk):
        try:
            consumer = Consumer.query.filter(Consumer.id == pk).one()
        except NoResultFound:
            return {"message": "Consumer could not be found."}, 400
        consumer_result = consumer_schema.dump(consumer)
        return jsonify(consumers_schema.dump(consumer_result))

    @app.route("/providers/", methods=['GET'])
    def get_providers():
        all_providers = Provider.query.all()
        return jsonify(providers_schema.dump(all_providers))

    @app.route("/providers/<int:pk>", methods=['GET'])
    def get_provider(pk):
        try:
            provider = Provider.query.filter(Consumer.id == pk).one()
        except NoResultFound:
            return {"message": "Provider could not be found."}, 400
        provider_result = provider_schema.dump(provider)
        return jsonify(provider_schema.dump(provider_result))

    @app.route("/consumers", methods=['POST'])
    def post_consumer():
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            data = consumer_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        category = data['category']
        category_new = Category.query.filter_by(name=category).first()
        if category_new is None:
            category_in = Category(name=category)
            db.session.add(category_in)
        consumer = Consumer(name=data['name'], bin=data['bin'], password=data['password'], country=data['country'], city=data['city'], adress=data['adress'], category=data['category'])
        db.session.add(consumer)
        db.session.commit()
        result = consumer_schema.dump(Consumer.query.get(consumer.id))
        return {'massage':'Created new consumer', 'consumer': result}
    
    @app.route("/providers", methods=['POST'])
    def post_provider():
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            data = provider_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        category = data['category']
        category_new = Category.query.filter_by(name=category).first()
        if category_new is None:
            category_in = Category(name=category)
            db.session.add(category_in)
        provider = Provider(name=data['name'], bin=data['bin'], password=data['password'], country=data['country'], city=data['city'], adress=data['adress'], category=data['category'])
        db.session.add(provider)
        db.session.commit()
        result = consumer_schema.dump(Provider.query.get(provider.id))
        return {'massage':'Created new Provider', 'provider': result}

def main():
    registered_handlers(app)
    db.create_all()
    app.run(debug=True, port=5000)



if __name__ == "__main__":
    main()
