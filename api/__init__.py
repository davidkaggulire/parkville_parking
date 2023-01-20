from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required

# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app = Flask(__name__)
api = Api(app)
app.config.from_object(app_config["testing"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
# db.create_all()

# to eliminate circular imports
from .routes import vehicle_routes
from .routes import charge_routes
from .routes import cartype_routes
from .routes import parking_routes
from .routes import clinic_routes, battery_routes, admin_routes
from .routes import user_routes
from .models import BlacklistToken


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    print("this is jti")
    print(jti)
    print(jwt_payload)
    token = db.session.query(BlacklistToken.id).filter_by(token=jti).scalar()

    return token is not None


@app.route("/protected", methods=["GET"])
@jwt_required()
# @token_required
def protected():
    return jsonify(hello="world")
