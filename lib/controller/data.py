from flask import request
from flask_restful import Resource
import pandas as pd

from lib.data import InputFile

class ImportData(Resource):
  def get(self):
    return {"message": "halo"}

  def post(self):
    file = request.files.get("data")
    
    df = pd.read_csv(file)
    data = InputFile(dataframe = df)

    return {"message": "OK"}