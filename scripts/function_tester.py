import pandas as pd

train = pd.read_csv("../assets/train.csv", index_col=0)
print(1 - train["written_precoup"].mean())

test = pd.read_csv("../assets/test.csv", index_col=0)
print(1 - test["written_precoup"].mean())
