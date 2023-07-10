from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from supabase import create_client, Client

# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# def create_app(config_name):
app = Flask(__name__)
api = Api(app)
app.config.from_object(app_config["production"])
# app.config.from_object(app_config[config_name])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

with app.app_context():
    engine = db.engine
    session = db.session
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    db.create_all()
    # return app

# to eliminate circular imports
from .routes import vehicle_routes
from .routes import charge_routes
from .routes import cartype_routes
from .routes import parking_routes
from .routes import clinic_routes, battery_routes, admin_routes
from .routes import user_routes
from .models import BlacklistToken


# @jwt.token_in_blocklist_loader
# def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
#     jti = jwt_payload["jti"]
#     print("this is jti")
#     print(jti)
#     print(jwt_payload)
#     token = db.session.query(BlacklistToken.id).filter_by(token=jti).scalar()

#     return token is not None


# @app.route("/protected", methods=["GET"])
# @jwt_required()
# # @token_required
# def protected():
#     return jsonify(hello="world")
