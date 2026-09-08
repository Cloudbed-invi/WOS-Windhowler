import re

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# Add get_expected_damage helper
helper_funcs = """def load_formulas():
    import json, os
    try:
        with open("formulas.json", "r") as f:
            return json.load(f)
    except:
        return {"A": 591.44, "B": 4.18, "TIER_FORMULAS": []}

def get_expected_damage(level):
    import numpy as np
    config = load_formulas()
    for tier in config.get("TIER_FORMULAS", []):
        if tier["range"][0] <= level <= tier["range"][1]:
            c = tier["coeffs"]
            expected = c[0]*(level**3) + c[1]*(level**2) + c[2]*level + c[3]
            return expected, tier.get("provisional", True), False
            
    A = config.get("A", 591.44)
    B = config.get("B", 4.18)
    expected = A * np.power(level, B)
    return expected, True, True

def run_ocr"""
code = code.replace("def run_ocr", helper_funcs)

# Update run_ocr sanity check
old_sanity = """                # Check expected damage boundary (Monotonic/Curve Deviation Check)
                expected = 602.34 * np.power(level, 4.1763)
                if expected > 0:
                    error = abs(damage - expected) / expected
                    if error > 0.50:  # If it deviates wildly (50%+) from the baseline power curve
                        flags.append(f"Curve Deviation > 50% (Expected ~{int(expected)})")"""

new_sanity = """                # Check expected damage using tier-aware formulas
                expected, is_provisional, is_fallback = get_expected_damage(level)
                if expected > 0:
                    error = abs(damage - expected) / expected
                    tolerance = 0.50 if (is_provisional or is_fallback) else 0.25
                    
                    if error > tolerance:
                        tier_status = "Provisional Tier/Fallback" if (is_provisional or is_fallback) else "Confirmed Tier"
                        flags.append(f"{tier_status} Deviation > {int(tolerance*100)}% (Expected ~{int(expected)})")"""

code = code.replace(old_sanity, new_sanity)

# Output formulas.json in run_ml_and_export
old_export = """    with open("exact_levels.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    return {"""

new_export = """    with open("exact_levels.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    formulas_config = {
        "A": extrapolate_A,
        "B": extrapolate_B,
        "TIER_BOUNDARIES": tier_boundaries,
        "BOUNDARY_METADATA": boundary_metadata,
        "TIER_FORMULAS": tier_formulas
    }
    with open("formulas.json", "w", encoding="utf-8") as f:
        json.dump(formulas_config, f, indent=2)
        
    return {"""
code = code.replace(old_export, new_export)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
