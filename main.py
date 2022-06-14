from flask import Flask
import sqlalchemy
import json
import jsonschema

from handlers import register_handlers


def main():
    with open("config.json") as config:
        config = json.load(config)

    with open("config.schema.json") as schema:
        schema = json.load(schema)

    try:
        jsonschema.validate(config, schema)
    except jsonschema.ValidationError as error:
        print("schmema validation failed: {}".format(error))
        exit(1)

    app = Flask(__name__)
    register_handlers(app)
    app.run(host=config['server']['host'], port=config['server']['port'])


if __name__ == "__main__":
    main()
