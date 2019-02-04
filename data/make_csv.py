import pandas as pd

df = pd.read_json("current_measurements.json")

df.to_csv("measurements.csv", index=False)
