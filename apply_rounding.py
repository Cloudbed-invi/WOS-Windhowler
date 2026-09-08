import re

with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# Fix rounding in both extrapolation blocks
old_block = """            all_levels[lvl] = {
                "start": round(start),
                "window": round(next_start - start),
                "confirmed": False,
                "extrapolated": True
            }"""

new_block = """            all_levels[lvl] = {
                "start": round(start),
                "window": round(next_start) - round(start),
                "confirmed": False,
                "extrapolated": True
            }"""

code = code.replace(old_block, new_block)

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
