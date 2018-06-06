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
    model = None

    def __init__(self, df=None):
        self.df = df

    @classmethod
    def predict_day(cls, model_location, x):
        '''
        predict will load the model, prepare the data for the model and predict the next [lookback] datapoints
        x is a list of lookback * 2 length
        model location is the path to the persisted model
        predict(model_location, x) -> list(length lookback)
        '''
        cls.model = cls.model or joblib.load(model_location)
        prepared = []
        for i in range(cls.lookback):
            prepared.append(x[i:i + cls.lookback])
        return cls.model.predict(prepared)[-1]

    def train(self):
        self.prepare_data()
        self.build_train_test()
        self.model = LinearRegression()
        self.model.fit(self.x_train, self.y_train)

    def evaluate(self, actual, new_values):
        predicted = self.predict(new_values)
        return mean_absolute_error(actual, predicted)

    def predict(self, x):
        '''predict requires a parameter that is of shape: (lookback, lookback)'''
        return self.model.predict(x)

    def prepare_data(self):
        x, y = [], []
        for i in range(self.lookback, len(self.df) - self.lookback):
            x.append(self.df[i - self.lookback:i])
            y.append(self.df[i:i + self.lookback])
        self.x = x
        self.y = y

    def build_train_test(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x, self.y, test_size=self.test_size, shuffle=False)

    def load_model(self, model_location):
        self.model = joblib.load(model_location)

    def save_model(self, model_location):
        joblib.dump(self.model, model_location)
