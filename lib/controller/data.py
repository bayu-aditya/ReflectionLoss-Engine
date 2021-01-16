from flask import request
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
        "message": "halo",
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