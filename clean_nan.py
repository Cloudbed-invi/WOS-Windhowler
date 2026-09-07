import pandas as pd

df = pd.read_csv("data.csv")
original_len = len(df)

# Drop any rows with NaN in Level, Percent, or Damage
df_clean = df.dropna(subset=['Level', 'Percent', 'Damage'])

df_clean.to_csv("data.csv", index=False)
print(f"Cleaned {original_len - len(df_clean)} rows with missing data.")
