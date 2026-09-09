with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

old_regex = """        damage_match = re.search(r'dealt\s+([\d,]+)\s+damage', full_text, re.IGNORECASE)
        percent_match = re.search(r'reaching\s+(\d+)%', full_text, re.IGNORECASE)
        level_match = re.search(r'Lv[.,\s_]*(\d+)', full_text, re.IGNORECASE)
        
        

        try:
            damage_str = damage_match.group(1) if damage_match else None
            damage = int(damage_str.replace(',', '')) if damage_str else None
            percent_str = percent_match.group(1) if percent_match else None"""

new_regex = """        # Multi-language robust regexes (English, Polish, French, Spanish, German, etc.)
        damage_match = re.search(r'(?:dealt|zadac|zadać|inflig|caus|schaden|damage|obrazen|obrażeń|degat|dégât|dano|daño)[^\d]*([\d,\s\.]{4,})', full_text, re.IGNORECASE)
        percent_match = re.search(r'(\d+)\s*%', full_text, re.IGNORECASE)
        level_match = re.search(r'(?:Lv|poz|niv|level|nivel)[.,\s_]*(\d+)', full_text, re.IGNORECASE)
        
        try:
            import re
            damage_str = damage_match.group(1) if damage_match else None
            damage = int(re.sub(r'[^\d]', '', damage_str)) if damage_str else None
            percent_str = percent_match.group(1) if percent_match else None"""

code = code.replace(old_regex, new_regex)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
