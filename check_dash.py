with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if "Data Coverage" in line or "df_coverage" in line:
            print(f"Line {i}: {line.strip()}")
