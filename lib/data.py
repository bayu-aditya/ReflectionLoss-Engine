import pandas as pd
import numpy as np

class InputFile:
  """
  Input file from filename
  """
  def __init__(self, filename: str):
    """
    initialization import file from filename
    """
    self._data = pd.read_csv(filename)

    self.frequency = []
    self._s11 = []
    self._s12 = []
    self._s21 = []
    self._s22 = []

    for _, row in self._data.iterrows():
      self.frequency.append(row["frequency"])
      self._s11.append(complex(row["s11r"], row["s11i"]))
      self._s12.append(complex(row["s12r"], row["s12i"]))
      self._s21.append(complex(row["s21r"], row["s21i"]))
      self._s22.append(complex(row["s22r"], row["s22i"]))