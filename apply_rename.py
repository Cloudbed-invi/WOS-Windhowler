import re

with open("wos-formula-refiner.html", "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("Old ML Model:", "Confirmed Fit:")
code = code.replace("Old ML Model (Huber)", "Confirmed Fit")

with open("wos-formula-refiner.html", "w", encoding="utf-8") as f:
    f.write(code)
