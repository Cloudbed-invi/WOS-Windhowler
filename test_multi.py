import re

texts = [
    "Udalo Ci sie zadac 102 067 675 obrazen Wyjacemu Wiatrowi oraz osiagnac 58% proby na poz. 18.",
    "You dealt 102,067,675 damage to Howling Wind and reached 58% on Lv. 18.",
    "Tu as inflige 102 067 675 degats a Vent Hurlant et atteint 58% au Niv. 18.",
    "Has infligido 102.067.675 de dano a Viento Aullante y alcanzado el 58% en el Nivel 18."
]

for text in texts:
    dmg = re.search(r'(?:dealt|zadac|inflig|causa|machen|dano|degat|damage|obrazen)[^\d]*([\d,\s\.]{5,})', text, re.IGNORECASE)
    pct = re.search(r'(\d+)\s*%', text)
    lvl = re.search(r'(?:Lv|poz|Niv|Level|Nivel)[.,\s_]*(\d+)', text, re.IGNORECASE)
    
    print(f"TEXT: {text[:30]}...")
    print("  Dmg:", dmg.group(1).strip() if dmg else None)
    print("  Pct:", pct.group(1) if pct else None)
    print("  Lvl:", lvl.group(1) if lvl else None)
