import pandas as pd
import os
from humidity_linear_regression import HumidityLinearRegression

with open(os.path.join(os.path.dirname(__file__), "../../data/current_measurements.json")) as file:
    df = pd.read_json(file)

print(df.head())
# reverse the order, the data was ordered by DATE DESC, but we want the more recent data to be used in the test set

lin_reg = HumidityLinearRegression(df.humidity.values[::-1])
lin_reg.train()
print(f"MAE (training): {lin_reg.evaluate(lin_reg.y_train, lin_reg.x_train)}")
print(f"MAE (training): {lin_reg.evaluate(lin_reg.y_test, lin_reg.x_test)}")

lin_reg.save_model('models/hum_lin_reg.pkl')
