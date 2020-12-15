import numpy as np
import pandas as pd

from lib import InputFile
from lib.core.calculate import (
  reflectance, 
  transmitance, 
  delta_const, 
  relative_permeability, 
  relative_permitivity, 
  impedance, 
  absorption
)

d = 4.74e-3
# data = InputFile("./data/data_csv_ujicoba.csv")
data = InputFile("./data/11-4.74_preprocess.txt")

resultRL = []
for idx, freq in enumerate(data.frequency):
  s11 = data.s11[idx]
  s21 = data.s21[idx]
  
  R = reflectance(s11, s21)
  T = transmitance(s11, s21)
  print(np.absolute(R), np.absolute(T), np.absolute(R) + np.absolute(T))
  delta = delta_const(d, T)
  mr = relative_permeability(R, delta)
  er = relative_permitivity(mr, T, d)
  Z = impedance(freq, d, mr, er)
  RL = absorption(Z)

  resultRL.append(RL)
resultRL = np.array(resultRL)

concat = np.vstack((data.frequency, resultRL)).T

resultDF = pd.DataFrame(data=concat, columns=["frequency", "reflection_loss"])
resultDF.to_csv("./result/result2.csv", index=None)