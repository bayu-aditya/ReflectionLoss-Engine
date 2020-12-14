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
data = InputFile("./data/data_csv_ujicoba.csv")

R = reflectance(data._s11[0], data._s21[0])
print(R)

T = transmitance(data._s11[0], data._s21[0])
print(T)

delta = delta_const(d, T)
print(delta)

mr = relative_permeability(R, delta)
print(mr)

er = relative_permitivity(mr, T, d)
print(er)

Z = impedance(1.0e9, d, mr, er)
print(Z)

RL = absorption(Z)
print(RL)