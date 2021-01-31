from flask import request, make_response
from flask_restful import Resource
import pandas as pd

from lib.data import InputFile
from lib.core.error import CustomException

class ImportData(Resource):
  def get(self):
    try:
      key = request.headers.get("key")

      data = InputFile.load_from_redis(key)
      return {
        "message": "OK, experiment data",
        "data": data.dataframe.to_dict()
      }

    except Exception as e:
      return CustomException(e)

  def post(self):
    try:
      file = request.files.get("data")
      
      df = pd.read_csv(file)
      data = InputFile(dataframe = df)

      key = data.save_to_redis()
      return {
        "message": "OK",
        "key": key,
      }

    except Exception as e:
      return CustomException(e)


class DownloadExperimentData(Resource):
  def get(self):
    try:
      key = request.headers.get("key")

      data = InputFile.load_from_redis(key)

      resp = make_response(data.dataframe.to_csv(index=None))
      resp.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
      resp.headers["Content-Disposition"] = "attachment; filename=experiment_dataset.csv"
      resp.headers["Content-Type"] = "text/csv"
      return resp

    except Exception as e:
      return CustomException(e)


class ImportDataSimulation(Resource):
  def get(self):
    try:
      key = request.headers.get("key")

      data = InputFile.load_from_redis(key, experiment_mode=False)
      return {
        "message": "OK, simulation data", 
        "data": data.dataframe.to_dict()
      }

    except Exception as e:
      return CustomException(e)

  def post(self):
    try:
      file = request.files.get("data")

      df = pd.read_csv(file)
      data = InputFile(dataframe = df, experiment_mode = False)

      key = data.save_to_redis()
      return {
        "message": "OK",
        "key": key
      }

    except Exception as e:
      return CustomException(e)


class DownloadSimulationParameterData(Resource):
  def get(self):
    try:
      key = request.headers.get("key")

      data = InputFile.load_from_redis(key, experiment_mode = False)

      resp = make_response(data.dataframe.to_csv(index=None))
      resp.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
      resp.headers["Content-Disposition"] = "attachment; filename=simulation_parameter.csv"
      resp.headers["Content-Type"] = "text/csv"
      return resp

    except Exception as e:
      return CustomException(e)