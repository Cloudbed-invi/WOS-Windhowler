import re
with open("wos-formula-refiner.html", "r", encoding="utf-8") as f:
    html = f.read()
    matches = re.findall(r"<input .*?>", html)
    for m in matches:
        print(m)
