from flask.globals import request
from flask_restful import Resource
import numpy as np
import pandas as pd

from lib.data import InputFile
from lib.core.calculate import (
  absorption, delta_const, 
  impedance, 
  reflectance, 
  relative_permeability,
  relative_permitivity, 
  transmitance
)

class CalculateSimulationController(Resource):
  def post(self):
    req_json: dict = request.get_json()

    freq_start = req_json["frequency"]["start"]
    freq_end = req_json["frequency"]["end"]
    freq_num = req_json["frequency"]["num_data"]
    freqs = np.linspace(freq_start, freq_end, freq_num)

    d = req_json["absorber_thickness"]
    mr_real = req_json["relative_permeability"]["real"]
    mr_imag = req_json["relative_permeability"]["imag"]
    mr = np.complex(mr_real, mr_imag)

    er_real = req_json["relative_permitivity"]["real"]
    er_imag = req_json["relative_permitivity"]["imag"]
    er = np.complex(er_real, er_imag)

    show_impedance = req_json["option"]["show"]["impedance"]
    show_absorption = req_json["option"]["show"]["absorption"]

    Zreal_data = list()
    Zimag_data = list()
    RL_data = list()

    for freq in freqs:
      Z = impedance(freq, d, mr, er)
      Zreal_data.append(Z.real)
      Zimag_data.append(Z.imag)

      RL = absorption(Z)
      RL_data.append(RL)

    response = dict()
    response["frequency"] = ['{:.2e}'.format(i) for i in freqs]
    if show_impedance:
      response["impedance"] = dict()
      response["impedance"]["real"] = Zreal_data
      response["impedance"]["imag"] = Zimag_data
    if show_absorption:
      response["reflection_loss"] = RL_data
    
    return response, 200


class CalculateExperimentController(Resource):
  def post(self):
    # reading formdata parameter
    file = request.files.get("data")
    thickness = np.float(request.form.get("thickness", 1))

    # get dataframe
    df = pd.read_csv(file)
    data = InputFile(dataframe=df)

    # initialize result lists
    resultFreq = list()
    resultR_r = list()
    resultR_i = list()
    resultT_r = list()
    resultT_i = list()
    resultMr_r = list()
    resultMr_i = list()
    resultEr_r = list()
    resultEr_i = list()
    resultZ_r = list()
    resultZ_i = list()
    resultRL = list()

    # calculate loop
    for idx, freq in enumerate(data.frequency):
      s11 = data.s11[idx]
      s21 = data.s21[idx]

      resultFreq.append('{:.2e}'.format(freq))

      R = reflectance(s11, s21)
      resultR_r.append(R.real)
      resultR_i.append(R.imag)
      
      T = transmitance(s11, s21)
      resultT_r.append(T.real)
      resultT_i.append(T.imag)

      delta = delta_const(thickness, T)

      mr = relative_permeability(R, delta)
      resultMr_r.append(mr.real)
      resultMr_i.append(mr.imag)
      
      er = relative_permitivity(mr, T, thickness)
      resultEr_r.append(er.real)
      resultEr_i.append(er.imag)

      Z = impedance(freq, thickness, mr, er)
      resultZ_r.append(Z.real)
      resultZ_i.append(Z.imag)
      
      RL = absorption(Z)
      resultRL.append(RL)

    return {
      "frequency": resultFreq,
      "reflectance": {
        "real": resultR_r,
        "imag": resultR_i,
      },
      "transmitance": {
        "real": resultT_r,
        "imag": resultT_i,
      },
      "relative_permeability": {
        "real": resultMr_r,
        "imag": resultMr_i,
      },
      "relative_permitivity": {
        "real": resultEr_r,
        "imag": resultEr_i,
      },
      "impedance": {
        "real": resultZ_r,
        "imag": resultZ_i,
      },
      "reflection_loss": resultRL
    }