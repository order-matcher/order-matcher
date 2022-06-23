from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from handlers.handlers import registered_handlers
# import sqlalchemy
# import json
# import jsonschema
import os



    # with open("config.json") as config:
    #     config = json.load(config)

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

db = SQLAlchemy(app)

def main():
    registered_handlers(app)
    db.create_all()
    app.run(debug=True, port=5000)



if __name__ == "__main__":
    main()
