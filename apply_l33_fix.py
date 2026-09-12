import pandas as pd
import wos_pipeline

df = pd.read_csv("data.csv")
new_row = {"File": "media_1788925556344.png", "Name": "Community", "Level": 33, "Percent": 60.0, "Damage": 1487367636, "Confidence": 1.0}
df_new = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
df_new.to_csv("data.csv", index=False)

wos_pipeline.run_ml_and_export()
