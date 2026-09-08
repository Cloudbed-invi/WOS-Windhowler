import pandas as pd
df = pd.read_csv("data.csv")
print("=== data.csv Integrity Check ===")
print("Shape:", df.shape)
print("\nTail (5):")
print(df.tail(5))
print("\n=== DictWriter usages in admin_dashboard.py ===")
with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    for line in f:
        if "csv.DictWriter" in line:
            print(line.strip())
