import numpy as np

lambda0 = 2.75
lambdaC = 3.98
c = 3.0e8

def reflectance(s11: np.complex, s21: np.complex) -> np.complex:
  """
  calculate reflectance coefficient from S constant
  """
  X = (s11**2 - s21**2 + 1) / (2 * s11)
  return X + np.sqrt(X**2 - 1)

def transmitance(s11: np.complex, s21: np.complex) -> np.complex:
  """
  calculate transmitance coefficient from S constant
  """
  R = reflectance(s11, s21)
  return (s11 + s21 - R) / (1 - (s11 + s21) * R)

def delta_const(d: np.float, transmitance: np.complex) -> np.complex:
  """
  calculate delta coefficient
  """
  delta_square_inv = -((1.0 / (2*np.pi*d)) * np.log(1.0 / transmitance))**2
  return np.sqrt(1.0 / delta_square_inv)

def relative_permeability(
    reflectance: np.complex, 
    delta_coef: np.complex, 
    lambda0: float = lambda0, 
    lambdaC: float = lambdaC
  ):
  """
  calculate relative permeability
  """
  return (
    (1.0 + reflectance) /
    (delta_coef * (1.0 - reflectance) * np.sqrt(complex((1.0 / lambda0**2) - (1.0 / lambdaC**2))))
  )

def relative_permitivity(
    relative_permeability: np.complex, 
    transmitance: np.complex, 
    d: np.float, 
    lambda0: float = lambda0, 
    lambdaC: float = lambdaC
  ) -> np.complex:
  """
  calculate relative permitivity
  """
  return (
    (lambda0**2 / relative_permeability) *
    ((1.0 / lambdaC**2) - ((1.0 / (2.0*np.pi*d)) * np.log(1.0 / transmitance))**2)
  )

def impedance(frequency: np.float, d: np.float, relative_permeability: np.complex, relative_permitivity: np.complex) -> np.complex:
  """
  calculate impedance
  """
  return (
    np.sqrt(relative_permeability / relative_permitivity) * 
    np.tanh(
      np.complex(0, ((2.0*np.pi*frequency*d) / c) * np.sqrt(relative_permeability*relative_permitivity))
    )
  )

def absorption(impedance: np.complex) -> np.float:
  """
  calculate absorption
  """
  return -20.0 * np.log10((np.absolute(impedance) - 1.0) / (np.absolute(impedance) + 1.0))
