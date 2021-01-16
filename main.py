import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from lib.service import redis_client
from lib.controller import ImportData, CalculateSimulationController, CalculateExperimentController

app = Flask(__name__)
CORS(app)
api = Api(app)

redis_pass = os.getenv("REDIS_PASS")
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_db = os.getenv("REDIS_DB")

app.config["REDIS_URL"] = "redis://:{}@{}:{}/{}".format(redis_pass, redis_host, redis_port, redis_db)

redis_client.init_app(app)

base_path = "/api"

api.add_resource(ImportData, base_path + "/data")
api.add_resource(CalculateSimulationController, base_path + "/calculate/simulation")
api.add_resource(CalculateExperimentController, base_path + "/calculate/experiment")