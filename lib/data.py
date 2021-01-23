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
    experiment_mode: bool = True
  ):
    """
    initialization import file from filename
    """
    if filename:
      self._data = pd.read_csv(filename, delim_whitespace=True)
    if dataframe is not None:
      self._data = dataframe

    self.frequency = []

    # eksperiment mode
    self.s11 = []
    self.s21 = []

    # simulation mode
    self.mr = []
    self.er = []

    if experiment_mode:
      for _, row in self._data.iterrows():
        self.frequency.append(row["frequency"])
        self.s11.append(complex(row["s11r"], row["s11i"]))
        self.s21.append(complex(row["s21r"], row["s21i"]))

      self.frequency = np.array(self.frequency)
      self.s11 = np.array(self.s11)
      self.s21 = np.array(self.s21)
      
      
    else:
      for _, row in self._data.iterrows():
        self.frequency.append(row["frequency"])
        self.mr.append(complex(row["mr_r"], row["mr_i"]))
        self.er.append(complex(row["er_r"], row["er_i"]))
      
      self.frequency = np.array(self.frequency)
      self.mr = np.array(self.mr)
      self.er = np.array(self.er)

  @property
  def dataframe(self) -> pd.DataFrame:
    return self._data

  def save_to_redis(self) -> str:
    bytes = zlib.compress(pickle.dumps(self.dataframe))

    key = generate_random(32)
    redis_client.set(key, bytes, 3600*24)
    return key

  @classmethod
  def load_from_redis(cls, key:str, experiment_mode:bool = True) -> "InputFile":
    if key is None:
      raise Exception("key is none", 400)

    bytes = redis_client.get(key)
    if bytes is None:
      raise Exception("data not found", 404)

    rehydrate_df = pickle.loads(zlib.decompress(bytes))
    return cls(dataframe = rehydrate_df, experiment_mode = experiment_mode)