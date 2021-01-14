from flask.globals import request
from flask_restful import Resource
import numpy as np

from lib.core.calculate import absorption, impedance

class CalculateController(Resource):
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
    if show_impedance:
      response["impedance"] = dict()
      response["impedance"]["real"] = Zreal_data
      response["impedance"]["imag"] = Zimag_data
    if show_absorption:
      response["absorption"] = RL_data
    
    return response, 200