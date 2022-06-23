from flask import Flask, jsonify, request
from database.schema import *
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound
from database.model import *
from tender import db

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

    @app.route("/orders/", methods=['GET'])
    def get_orders():
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
        order = Order(title=data['title'], description=data['description'], 
        date_start=data['date_start'], date_end=data['date_end'], contact_person=data['contact_person'],
        phone=data['phone'], costs=data['costs'], currency=data['currency'], consumer=data["consumer"])
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

    @app.route("/consumers/add", methods=['POST'])
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
        consumer = Consumer(name=data['name'], country=data['country'], city=data['city'], adress=data['adress'], category=data['category'])
        db.session.add(consumer)
        db.session.commit()
        result = consumer_schema.dump(Consumer.query.get(consumer.id))
        return {'massage':'Created new consumer', 'consumer': result}
    @app.route("/providers/add", methods=['POST'])
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
        provider = Provider(name=data['name'], country=data['country'], city=data['city'], adress=data['adress'], category=data['category'])
        db.session.add(provider)
        db.session.commit()
        result = consumer_schema.dump(Provider.query.get(provider.id))
        return {'massage':'Created new Provider', 'provider': result}