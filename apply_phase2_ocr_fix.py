import re

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

old_ocr_check = """                # Check expected damage using tier-aware formulas
                expected, is_provisional, is_fallback = get_expected_damage(level)
                if expected > 0:
                    error = abs(damage - expected) / expected"""

new_ocr_check = """                # Check expected damage using tier-aware formulas
                expected_start, is_provisional, is_fallback = get_expected_damage(level)
                expected_next, _, _ = get_expected_damage(level + 1)
                expected = expected_start + (percent / 100.0) * (expected_next - expected_start)
                if expected > 0:
                    error = abs(damage - expected) / expected"""

code = code.replace(old_ocr_check, new_ocr_check)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
