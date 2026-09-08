import pandas as pd
df = pd.read_csv("data.csv")
if "Confidence" not in df.columns:
    df["Confidence"] = ""
    df.to_csv("data.csv", index=False)
