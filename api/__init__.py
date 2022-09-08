from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_migrate import Migrate

import os

# app = Flask(__name__)
# api = Api(app)

# CORS(app)
# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

app = Flask(__name__)
api = Api(app)
app.config.from_object(app_config["testing"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)   
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# db.create_all()

# to eliminate circular imports
from api.routes import vehicle_routes
from api.routes import charge_routes





