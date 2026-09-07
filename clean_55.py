import pandas as pd
import wos_pipeline

df = pd.read_csv("data.csv")
# Keep only rows where Level is not 55
df_clean = df[df['Level'] != 55]

df_clean.to_csv("data.csv", index=False)
print(f"Removed {len(df) - len(df_clean)} anomalous rows for Level 55.")

# Recalculate AI formulas
wos_pipeline.run_ml_and_export()
print("Recalculated ML formulas successfully.")
