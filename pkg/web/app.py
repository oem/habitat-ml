from flask import Flask, render_template
import requests
import json
import os
from .helpers.data_preparation import prepare_data

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


if __name__ == '__main__':
    app.run()
