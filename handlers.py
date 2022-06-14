from flask_json_schema import JsonSchema, JsonValidationError
from flask import Flask, request, jsonify


# TODO:
# Создать хендлеры для создания всех сущгостей (Consumer, ...)
# Создать схемы для этих хендлеров (важно пордумать все обязтальные поля и написать к ним описание)
# Сделать механизм подгрузки схем из файлов (должна быть директория, в которой хранятся все схема и при запуске они подгружаются в некий словарь)

# Подключить sqlalchemy к sqlite, чтобы можно было в хендлерах уже использовать подключение к БД


def register_handlers(app: Flask):
    schema = JsonSchema(app)

    order_schema = {
        "properties": {
            "name" : {'type' : 'string'},
            "description" : {'type' : 'string'}
        },
        'required': [
            'name'
        ]
    }

    @app.errorhandler(JsonValidationError)
    def validation_error(e):
        return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]})

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/create_order", methods=['POST'])
    @schema.validate()
    def create_order():
        request_data = request.get_json()
        return request_data
