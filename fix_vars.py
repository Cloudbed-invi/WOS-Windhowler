with open("wos-formula-refiner.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix variable declarations
html = html.replace("let exactLvl = null, exactPct = null, exactConfirmed = false, exactExtrapolated = false;",
                    "let exactLvl = null, exactPct = null, exactConfirmed = false, exactExtrapolated = false, exactClustered = false;")
html = html.replace("if (data.extrapolated) exactExtrapolated = true;",
                    "if (data.extrapolated) exactExtrapolated = true;\n          if (data.clustered) exactClustered = true;")

# Fix the badge logic that I injected earlier
html = html.replace("} else if (exact.clustered) {", "} else if (exactClustered) {")

with open("wos-formula-refiner.html", "w", encoding="utf-8") as f:
    f.write(html)
