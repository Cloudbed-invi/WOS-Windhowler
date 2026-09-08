import pandas as pd
import numpy as np
from sklearn.linear_model import HuberRegressor

df = pd.read_csv("data.csv").drop_duplicates(subset=['Level', 'Percent', 'Damage'])
levels = df['Level'].unique()
levels.sort()
confirmed_data = {}
for lvl in levels:
    if lvl == 1: continue
    level_data = df[df['Level'] == lvl]
    if len(level_data["Percent"].unique()) < 2: continue
    X = (level_data['Percent'] / 100.0).values.reshape(-1, 1)
    y = level_data['Damage'].values
    model = HuberRegressor(epsilon=1.35)
    model.fit(X, y / 1_000_000.0)
    confirmed_data[int(lvl)] = (model.intercept_ + model.coef_[0]) * 1_000_000

for k,v in confirmed_data.items():
    print(f"Level {k}: {v:,.0f}")
