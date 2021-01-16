import pandas as pd
import numpy as np
import pickle
import zlib

from lib.core.random import generate_random
from lib.service import redis_client

class InputFile:
  """
  Input file from filename or dataframe directly
  """
  def __init__(self, 
    filename: str = None,
    dataframe: pd.DataFrame = None,
  ):
    """
    initialization import file from filename
    """
    if filename:
      self._data = pd.read_csv(filename, delim_whitespace=True)
    if dataframe is not None:
      self._data = dataframe

    self._frequency = []
    self._s11 = []
    # self._s12 = []
    self._s21 = []
    # self._s22 = []

    for _, row in self._data.iterrows():
      self._frequency.append(row["frequency"])
      self._s11.append(complex(row["s11r"], row["s11i"]))
      # self._s12.append(complex(row["s12r"], row["s12i"]))
      self._s21.append(complex(row["s21r"], row["s21i"]))
      # self._s22.append(complex(row["s22r"], row["s22i"]))

    self.frequency = np.array(self._frequency)
    self.s11 = np.array(self._s11)
    # self.s12 = np.array(self._s12)
    self.s21 = np.array(self._s21)
    # self.s22 = np.array(self._s22)

  @property
  def dataframe(self) -> pd.DataFrame:
    return self._data

  def save_to_redis(self) -> str:
    bytes = zlib.compress(pickle.dumps(self.dataframe))

    key = generate_random(32)
    redis_client.set(key, bytes, 3600*24)
    return key

  @classmethod
  def load_from_redis(cls, key:str) -> "InputFile":
    if key is None:
      raise Exception("key is none", 400)

    bytes = redis_client.get(key)
    if bytes is None:
      raise Exception("data not found", 404)

    rehydrate_df = pickle.loads(zlib.decompress(bytes))
    return cls(dataframe = rehydrate_df)