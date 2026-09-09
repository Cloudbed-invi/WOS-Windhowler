import re
with open("wos-formula-refiner.html", "r", encoding="utf-8") as f:
    html = f.read()
    matches = re.findall(r"<div class=\"input-group\">.*?</div>", html, re.DOTALL)
    for m in matches[:2]:
        print(m)
