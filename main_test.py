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

d = 4.74e-1 # cm
data = InputFile("./data/11-4.74_preprocess.txt")
# data._data.to_csv("./data/11-4.74_preprocess.csv", index=None)

resultR = []
resultT = []
resultDelta = []
resultMR = []
resultMR_r = []
resultMR_i = []
resultER = []
resultER_r = []
resultER_i = []
resultZ = []
resultRL = []
for idx, freq in enumerate(data.frequency):
  s11 = data.s11[idx]
  s21 = data.s21[idx]
  
  R = reflectance(s11, s21)
  T = transmitance(s11, s21)
  delta = delta_const(d, T)
  mr = relative_permeability(R, delta, freq)
  er = relative_permitivity(mr, T, d)
  Z = impedance(freq, d, mr, er)
  RL = absorption(Z)

  resultR.append(np.absolute(R))
  resultT.append(np.absolute(T))

  resultMR.append(np.absolute(mr))
  resultMR_r.append(mr.real)
  resultMR_i.append(mr.imag)

  resultER.append(np.absolute(er))
  resultER_r.append(er.real)
  resultER_i.append(er.imag)

  resultRL.append(RL)

concat = np.vstack((
  data.frequency, 
  resultR, 
  resultT, 
  resultMR, resultMR_r, resultMR_i,
  resultER, resultER_r, resultER_i,
  resultRL
  )).T

resultDF = pd.DataFrame(data=concat, columns=[
  "frequency", 
  "reflection_coeff",
  "transmission_coeff",
  "permeability_rel", "permeability_real", "permeability_imag",
  "permitivity_rel", "permitivity_real", "permitivity_imag",
  "reflection_loss"
  ])
resultDF.to_csv("./result/result.csv", index=None)