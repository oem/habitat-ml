from flask import Flask, render_template
import pandas as pd
import numpy as np
import requests
import json
import os
from ..models.humidity_linear_regression import HumidityLinearRegression

app = Flask(__name__)

token = os.environ['API_TOKEN']


@app.route('/', methods=['GET'])
def root():
    '''renders the index template with json embedded as data attribute'''
    measurements = requests.get(
        url=f"https://habitat-lifesupport.herokuapp.com/measurements?token={token}").json()[:72][::-1]
    last_24h, last_24h_predictions, next_24h_predictions = prepare_data(
        measurements)
    return render_template('index.html', measurements=json.dumps(last_24h), predictions=json.dumps(last_24h_predictions), next_day=json.dumps(next_24h_predictions))


def prepare_data(measurements):
    model_location = os.path.join(os.path.dirname(
        __file__), '../../models/hum_lin_reg.pkl')
    df = pd.DataFrame(measurements)
    last_24h = df[48:].to_dict('records')
    last_48h = df[24:].humidity.values
    previous_two_days = df[0:48].humidity.values
    last_24h_predictions = HumidityLinearRegression.predict_day(
        model_location, previous_two_days)
    last_24h_predictions = [
        {'humidity': n, 'measuredAt': last_24h[i]['measuredAt']} for i, n in enumerate(last_24h_predictions)]
    next_24h_predictions = HumidityLinearRegression.predict_day(
        model_location, last_48h)
    next_labels = [str(i) for i in pd.date_range(
        last_24h[-1]['measuredAt'], periods=25, freq='H')[1:]]
    next_24h_predictions = [
        {'humidity': n, 'measuredAt': next_labels[i]} for i, n in enumerate(next_24h_predictions)]
    return last_24h, last_24h_predictions, next_24h_predictions


if __name__ == '__main__':
    app.run()
