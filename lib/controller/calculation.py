from flask.globals import request
from flask.helpers import make_response
from flask_restful import Resource
import numpy as np
import pandas as pd
from scipy.signal._savitzky_golay import savgol_filter

from lib.core.error import CustomException
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
    try:
      download_result: str = request.headers.get("download_result")
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

      savgol_length = req_json["option"]["savgol_filter"]["window_length"]
      savgol_polyorder = req_json["option"]["savgol_filter"]["polyorder"]

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
      response["frequency"] = dict()
      response["frequency"]["label"] = ['{:.2e}'.format(i) for i in freqs]
      response["frequency"]["value"] = list(freqs)
      if show_impedance:
        response["impedance"] = dict()
        response["impedance"]["real"] = Zreal_data
        response["impedance"]["real_filter"] = list(savgol_filter(Zreal_data, savgol_length, savgol_polyorder))
        response["impedance"]["imag"] = Zimag_data
        response["impedance"]["imag_filter"] = list(savgol_filter(Zimag_data, savgol_length, savgol_polyorder))
      if show_absorption:
        response["reflection_loss"] = dict()
        response["reflection_loss"]["original"] = RL_data
        response["reflection_loss"]["filter"] = list(savgol_filter(RL_data, savgol_length, savgol_polyorder))

      # create dataframe for calculation result and download it
      if download_result == "true":
        df = pd.DataFrame(
          list(zip(
            freqs,
            Zreal_data, 
            Zimag_data,
            RL_data,
          )),
          columns=[
            "Frequency (Hz)",
            "Impedance Real", 
            "Impedance Imag",
            "Reflection Loss (dB)",
          ]
        )

        resp = make_response(df.to_csv(index=None))
        resp.headers["Content-Disposition"] = "attachment; filename=simulation_result.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
      
      return response, 200
  
    except Exception as e:
      return CustomException(e)


class CalculateSimulationWithDataController(Resource):
  def post(self):
    try:
      download_result: str = request.headers.get("download_result")
      key = request.headers.get("key")
      req_json: dict = request.get_json()

      data = InputFile.load_from_redis(key, experiment_mode=False)

      d = req_json["absorber_thickness"]

      show_impedance = req_json["option"]["show"]["impedance"]
      show_absorption = req_json["option"]["show"]["absorption"]

      savgol_length = req_json["option"]["savgol_filter"]["window_length"]
      savgol_polyorder = req_json["option"]["savgol_filter"]["polyorder"]

      Zreal_data = list()
      Zimag_data = list()
      RL_data = list()

      for (idx, freq) in enumerate(data.frequency):
        mr = data.mr[idx]
        er = data.mr[idx]

        Z = impedance(freq, d, mr, er)
        Zreal_data.append(Z.real)
        Zimag_data.append(Z.imag)

        RL = absorption(Z)
        RL_data.append(RL)

      response = dict()
      response["frequency"] = dict()
      response["frequency"]["label"] = ['{:.2e}'.format(i) for i in data.frequency]
      response["frequency"]["value"] = list(data.frequency)
      if show_impedance:
        response["impedance"] = dict()
        response["impedance"]["real"] = Zreal_data
        response["impedance"]["real_filter"] = list(savgol_filter(Zreal_data, savgol_length, savgol_polyorder))
        response["impedance"]["imag"] = Zimag_data
        response["impedance"]["imag_filter"] = list(savgol_filter(Zimag_data, savgol_length, savgol_polyorder))
      if show_absorption:
        response["reflection_loss"] = dict()
        response["reflection_loss"]["original"] = RL_data
        response["reflection_loss"]["filter"] = list(savgol_filter(RL_data, savgol_length, savgol_polyorder))

      # create dataframe for calculation result and download it
      if download_result == "true":
        df = pd.DataFrame(
          list(zip(
            data.frequency,
            Zreal_data, 
            Zimag_data,
            RL_data,
          )),
          columns=[
            "Frequency (Hz)",
            "Impedance Real", 
            "Impedance Imag",
            "Reflection Loss (dB)",
          ]
        )

        resp = make_response(df.to_csv(index=None))
        resp.headers["Content-Disposition"] = "attachment; filename=simulation_with_input_parameter_result.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp

      return response, 200

    except Exception as e:
      return CustomException(e)


class CalculateExperimentController(Resource):
  def post(self):
    try:
      # reading formdata parameter
      download_result: str = request.headers.get("download_result")
      key = request.headers.get("key")

      body_json = request.get_json()
      thickness = np.float(body_json["thickness"])
      lambda_0 = np.float(body_json["lambda_0"])
      lambda_C = np.float(body_json["lambda_C"])
      savgol_length = body_json["option"]["savgol_filter"]["window_length"]
      savgol_polyorder = body_json["option"]["savgol_filter"]["polyorder"]

      # get dataframe
      data = InputFile.load_from_redis(key)

      # initialize result lists
      resultFreqLabel = list()
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

        resultFreq.append(freq)
        resultFreqLabel.append('{:.2e}'.format(freq))

        R = reflectance(s11, s21)
        resultR_r.append(R.real)
        resultR_i.append(R.imag)
        
        T = transmitance(s11, s21)
        resultT_r.append(T.real)
        resultT_i.append(T.imag)

        delta = delta_const(thickness, T)

        mr = relative_permeability(R, delta, lambda_0, lambda_C)
        resultMr_r.append(mr.real)
        resultMr_i.append(mr.imag)
        
        er = relative_permitivity(mr, T, thickness, lambda_0, lambda_C)
        resultEr_r.append(er.real)
        resultEr_i.append(er.imag)

        Z = impedance(freq, thickness, mr, er)
        resultZ_r.append(Z.real)
        resultZ_i.append(Z.imag)
        
        RL = absorption(Z)
        resultRL.append(RL)

      # create dataframe for calculation result and download it
      if download_result == "true":
        df = pd.DataFrame(
          list(zip(
            data.frequency,
            resultR_r,
            resultR_i,
            resultT_r,
            resultT_i, 
            resultMr_r,
            resultMr_i,
            resultEr_r,
            resultEr_i,
            resultZ_r,
            resultZ_i,
            resultRL,
          )),
          columns=[
            "Frequency (Hz)",
            "Reflectance Real", 
            "Reflectance Imag",
            "Transmitance Real", 
            "Transmitance Imag",
            "Permeability Real",
            "Permeability Imag",
            "Permitivity Real",
            "Permitivity Imag",
            "Impedance Real",
            "Impedance Imag",
            "Reflection Loss (dB)",
          ]
        )

        resp = make_response(df.to_csv(index=None))
        resp.headers["Content-Disposition"] = "attachment; filename=experiment_result.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp

      return {
        "frequency": {
          "label": resultFreqLabel,
          "value": resultFreq,
        },
        "reflectance": {
          "real": resultR_r,
          "real_filter": list(savgol_filter(resultR_r, savgol_length, savgol_polyorder)),
          "imag": resultR_i,
          "imag_filter": list(savgol_filter(resultR_i, savgol_length, savgol_polyorder)),
        },
        "transmitance": {
          "real": resultT_r,
          "real_filter": list(savgol_filter(resultT_r, savgol_length, savgol_polyorder)),
          "imag": resultT_i,
          "imag_filter": list(savgol_filter(resultT_i, savgol_length, savgol_polyorder)),
        },
        "relative_permeability": {
          "real": resultMr_r,
          "real_filter": list(savgol_filter(resultMr_r, savgol_length, savgol_polyorder)),
          "imag": resultMr_i,
          "imag_filter": list(savgol_filter(resultMr_i, savgol_length, savgol_polyorder)),
        },
        "relative_permitivity": {
          "real": resultEr_r,
          "real_filter": list(savgol_filter(resultEr_r, savgol_length, savgol_polyorder)),
          "imag": resultEr_i,
          "imag_filter": list(savgol_filter(resultEr_i, savgol_length, savgol_polyorder)),
        },
        "impedance": {
          "real": resultZ_r,
          "real_filter": list(savgol_filter(resultZ_r, savgol_length, savgol_polyorder)),
          "imag": resultZ_i,
          "imag_filter": list(savgol_filter(resultZ_i, savgol_length, savgol_polyorder)),
        },
        "reflection_loss": {
          "original": resultRL,
          "filter": list(savgol_filter(resultRL, savgol_length, savgol_polyorder)),
        }
      }

    except Exception as e:
      return CustomException(e)