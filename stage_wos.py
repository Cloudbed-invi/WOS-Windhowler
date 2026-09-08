import re

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update get_expected_damage
old_get_expected = """def get_expected_damage(level):
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
    return expected, True, True"""

new_get_expected = """def get_expected_damage(level):
    import numpy as np
    config = load_formulas()
    tol_conf = config.get("TOLERANCE_CONFIRMED", 0.15)
    tol_prov = config.get("TOLERANCE_PROVISIONAL", 0.22)
    
    for tier in config.get("TIER_FORMULAS", []):
        if tier["range"][0] <= level <= tier["range"][1]:
            c = tier["coeffs"]
            expected = c[0]*(level**3) + c[1]*(level**2) + c[2]*level + c[3]
            if tier.get("provisional", True):
                return expected, "PROVISIONAL", tol_prov
            else:
                return expected, "CONFIRMED", tol_conf
            
    A = config.get("A", 591.44)
    B = config.get("B", 4.18)
    expected = A * np.power(level, B)
    return expected, "EXTRAPOLATED", 0.0 # 0 tolerance triggers unconditional review"""

code = code.replace(old_get_expected, new_get_expected)

# 2. Update run_ocr sanity check
old_ocr = """                # Check expected damage using tier-aware formulas
                expected_start, is_provisional, is_fallback = get_expected_damage(level)
                expected_next, _, _ = get_expected_damage(level + 1)
                expected = expected_start + (percent / 100.0) * (expected_next - expected_start)
                if expected > 0:
                    error = abs(damage - expected) / expected
                    tolerance = 0.50 if (is_provisional or is_fallback) else 0.25
                    
                    if error > tolerance:
                        tier_status = "Provisional Tier/Fallback" if (is_provisional or is_fallback) else "Confirmed Tier"
                        flags.append(f"{tier_status} Deviation > {int(tolerance*100)}% (Expected ~{int(expected)})")"""

new_ocr = """                # Check expected damage using tier-aware formulas
                expected_start, t_status, tol = get_expected_damage(level)
                expected_next, _, _ = get_expected_damage(level + 1)
                expected = expected_start + (percent / 100.0) * (expected_next - expected_start)
                
                if expected > 0:
                    error = abs(damage - expected) / expected
                    
                    if t_status == "EXTRAPOLATED":
                        flags.append(f"No tier fit for level {level} - manual review required")
                    elif error > tol:
                        tier_name = "Confirmed" if t_status == "CONFIRMED" else "Provisional"
                        flags.append(f"{tier_name} tier: {error*100:.1f}% deviation exceeds {int(tol*100)}% threshold")"""
code = code.replace(old_ocr, new_ocr)

# 3. Add tolerances to formulas.json export
old_export = """    formulas_config = {
        "A": extrapolate_A,
        "B": extrapolate_B,
        "TIER_BOUNDARIES": tier_boundaries,"""

new_export = """    formulas_config = {
        "TOLERANCE_CONFIRMED": 0.15,
        "TOLERANCE_PROVISIONAL": 0.22,
        "A": extrapolate_A,
        "B": extrapolate_B,
        "TIER_BOUNDARIES": tier_boundaries,"""
code = code.replace(old_export, new_export)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)

