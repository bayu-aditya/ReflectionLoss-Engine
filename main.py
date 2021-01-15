from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from lib.controller import ImportData, CalculateSimulationController, CalculateExperimentController

app = Flask(__name__)
CORS(app)
api = Api(app)

base_path = "/api"

api.add_resource(ImportData, base_path + "/import-data")
api.add_resource(CalculateSimulationController, base_path + "/calculate/simulation")
api.add_resource(CalculateExperimentController, base_path + "/calculate/experiment")