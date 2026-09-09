import re

text = "Udalo Ci sie zadac 102 067 675 obrazen Wyjacemu Wiatrowi oraz osiagnac 58% proby na poz. 18."

dmg_match = re.search(r'(?:dealt|zadac|zadać)\s+([\d,\s]+)\s+(?:damage|obrazen|obrażeń)', text, re.IGNORECASE)
pct_match = re.search(r'(?:reaching|osiagnac|osiągnąć)\s+(\d+)%', text, re.IGNORECASE)
lvl_match = re.search(r'(?:Lv|poz)[.,\s_]*(\d+)', text, re.IGNORECASE)

print("Damage:", dmg_match.group(1) if dmg_match else None)
print("Percent:", pct_match.group(1) if pct_match else None)
print("Level:", lvl_match.group(1) if lvl_match else None)
