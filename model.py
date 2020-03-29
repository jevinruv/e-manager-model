from numpy import nan
from numpy import isnan
from pandas import read_csv
from pandas import to_numeric

import pickle
import pandas as pd
import numpy as np
from fbprophet import Prophet
from datetime import datetime
from dateutil.relativedelta import relativedelta


def calculate_start_date(frequ):
    now = datetime.today().strftime('%Y-%m-%d')
    end_date = datetime.strptime(now, "%Y-%m-%d")
    start_date = datetime.strptime('2010-11-26', "%Y-%m-%d")

    num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    num_days = (end_date - start_date).days

    # print(num_days)
    # print(num_months)
    value = frequ

    if frequ.upper() == 'D':
      value = num_days
    elif frequ.upper() == 'M':
      value = num_months

    return value

def get_prediction_results(predict_freq, duration):

  is_annual = False

  if predict_freq.upper() == 'Y':
    duration = duration * 12
    predict_freq = 'M'
    is_annual = True
 
  duration_to_cal = calculate_start_date(predict_freq) + duration

  # load model
  with open("prophet_model.pkl", 'rb') as f:
    model = pickle.load(f)

  # Make a future dataframe
  future = model.make_future_dataframe(periods=duration_to_cal, freq=predict_freq)
  data_forecast = model.predict(future)

  data_forecast["Consumption"] = np.exp(data_forecast.yhat).round()
  data_forecast["Consumption_lower"] = np.exp(data_forecast.yhat_lower).round()
  data_forecast["Consumption_upper"] = np.exp(data_forecast.yhat_upper).round()

  result = data_forecast[["ds","Consumption_lower","Consumption", "Consumption_upper"]].tail(duration)

  if is_annual == True:
    result.index = result['ds'] 
    result = result.resample('Y').sum()

  return result

def train_model(df):
	# train model

	model = Prophet(daily_seasonality=True)
	model.stan_backend.logger = None
	model.fit(df)

	pkl_path = "prophet_model.pkl"
	with open(pkl_path, "wb") as f:
	    pickle.dump(model, f)
	print("Model Saved as File")


def get_prediction(predict_freq, duration):
	predicted_result = get_prediction_results(predict_freq, duration)

	return predicted_result.to_json(orient='records')
