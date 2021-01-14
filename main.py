from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from lib.controller import Test

app = Flask(__name__)
CORS(app)
api = Api(app)

base_path = "/api"

api.add_resource(Test, base_path + "/import-data")