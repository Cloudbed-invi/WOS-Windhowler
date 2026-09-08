import pandas as pd
import numpy as np

df = pd.read_csv("data.csv")

# Fill missing (NaN) confidences with 1.0 since they are strictly verified baseline data
if "Confidence" in df.columns:
    df["Confidence"] = df["Confidence"].fillna(1.0)
else:
    df["Confidence"] = 1.0

df.to_csv("data.csv", index=False)
print("Updated data.csv with 1.0 for all missing confidence values.")
