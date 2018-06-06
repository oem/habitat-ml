import math
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.externals import joblib


class HumidityLinearRegression():
    test_size = 0.2
    lookback = 24

    def __init__(self, df=None):
        self.df = df

    def train(self):
        self.prepare_data()
        self.model = LinearRegression()
        self.model.fit(self.x_train, self.y_train)

    def evaluate(self, actual, new_values):
        predicted = self.predict(new_values)
        return mean_absolute_error(actual, predicted)

    def predict(self, data):
        return self.model.predict(data)

    def prepare_data(self):
        X, y = [], []
        for i in range(self.lookback, len(self.df) - self.lookback):
            X.append(self.df[i - self.lookback:i])
            y.append(self.df[i:i + self.lookback])
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=self.test_size, shuffle=False)

    def load_model(self, model_location):
        self.model = joblib.load(model_location)

    def save_model(self, model_location):
        joblib.dump(self.model, model_location)
