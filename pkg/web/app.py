from flask import Flask, render_template
import requests
import json
import os
from ..models.humidity_linear_regression import HumidityLinearRegression
model = HumidityLinearRegression()
model.load_model(os.path.join(os.path.dirname(
    __file__), '../../models/hum_lin_reg.pkl'))

app = Flask(__name__)

token = os.environ['API_TOKEN']


@app.route('/', methods=['GET'])
def root():
    '''renders the index template with json embedded as data attribute'''
    measurements = requests.get(
        url=f"https://habitat-lifesupport.herokuapp.com/measurements?token={token}").json()[:24][::-1]
    print(measurements)
    return render_template('index.html', measurements=json.dumps(measurements), predictions=[23, 24])


if __name__ == '__main__':
    app.run()
