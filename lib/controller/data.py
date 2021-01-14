from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename
from io import StringIO
import pandas as pd

class Test(Resource):
  def get(self):
    return {"message": "halo"}

  def post(self):
    file = request.files.get("data")
    
    df = pd.read_csv(file)
    print(df.info())
    return {"message": "OK"}