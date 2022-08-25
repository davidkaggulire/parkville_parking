from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS

from resources.register import RegisterCar
from marshmallow import ValidationError

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400




api.add_resource(RegisterCar, '/')

if __name__ == '__main__':
    app.run(debug=True)
