import json
with open("formulas.json", "r") as f:
    d = json.load(f)
    print("| Level Pair | End vs. Start | Mismatch % | Flagged |")
    print("|------------|---------------|------------|---------|")
    for m in d["ADJACENT_MISMATCHES"]:
        print(f"| {m['Level Pair']} | {m['End N']:,} vs {m['Start N+1']:,} | {m['Mismatch %']}% | {m['Flagged']} |")
