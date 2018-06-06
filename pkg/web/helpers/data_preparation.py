import pandas as pd
import numpy as np
import os
from ...models.humidity_linear_regression import HumidityLinearRegression


def prepare_data(measurements):
    df = pd.DataFrame(measurements)
    last_24h = prepare_measurements_for_last_day(df)
    last_24h_predictions = prepare_predictions_for_last_day(df)
    next_24h_predictions = prepare_predictions_for_next_day(df)
    return last_24h, last_24h_predictions, next_24h_predictions


def prepare_measurements_for_last_day(df):
    return df[48:].to_dict('records')


def prepare_predictions_for_last_day(df):
    previous_two_days = df[0:48].humidity.values
    last_24h_predictions = HumidityLinearRegression.predict_day(
        model_location(), previous_two_days)
    last_24h = prepare_measurements_for_last_day(df)
    last_24h_predictions = [
        {'humidity': n, 'measuredAt': last_24h[i]['measuredAt']} for i, n in enumerate(last_24h_predictions)]
    return last_24h_predictions


def prepare_predictions_for_next_day(df):
    last_24h = prepare_measurements_for_last_day(df)
    last_48h = df[24:].humidity.values
    next_24h_predictions = HumidityLinearRegression.predict_day(
        model_location(), last_48h)
    next_labels = [str(i) for i in pd.date_range(
        last_24h[-1]['measuredAt'], periods=25, freq='H')[1:]]
    next_24h_predictions = [
        {'humidity': n, 'measuredAt': next_labels[i]} for i, n in enumerate(next_24h_predictions)]
    return next_24h_predictions


def model_location():
    return os.path.join(os.path.dirname(
        __file__), '../../../models/hum_lin_reg.pkl')
