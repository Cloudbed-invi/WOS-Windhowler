import pandas as pd
df = pd.read_csv("data.csv")
l25 = df[df["Level"] == 25]
print("Existing Level 25 data:")
print(l25[["Percent", "Damage"]])
