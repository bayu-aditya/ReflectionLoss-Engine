import pandas as pd
import numpy as np

class InputFile:
  """
  Input file from filename
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