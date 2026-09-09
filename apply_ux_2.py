import re

with open("wos-formula-refiner.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update body padding for safe areas
html = html.replace(
    "body { margin: 0; padding: 20px 15px; background: var(--bg); color: var(--text); }",
    "body { margin: 0; padding: max(20px, env(safe-area-inset-top)) max(15px, env(safe-area-inset-right)) max(20px, env(safe-area-inset-bottom)) max(15px, env(safe-area-inset-left)); background: var(--bg); color: var(--text); }"
)

# 2. Update theme toggle for better touch target & styling
old_toggle = """  /* Theme Toggle Button */
  .theme-toggle {
    position: absolute;
    top: 15px;
    right: 15px;
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: var(--text);
    padding: 5px;
  }"""

new_toggle = """  /* Theme Toggle Button */
  .theme-toggle {
    position: absolute;
    top: max(15px, env(safe-area-inset-top));
    right: max(15px, env(safe-area-inset-right));
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 50%;
    font-size: 20px;
    cursor: pointer;
    color: var(--text);
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    z-index: 100;
  }
  .theme-toggle:hover { background: var(--border); }
"""
html = html.replace(old_toggle, new_toggle)

# 3. Increase action-btn touch target
html = html.replace(
    "button.action-btn { width: 100%; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; transition: opacity 0.2s; }",
    "button.action-btn { width: 100%; min-height: 48px; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: transform 0.1s, opacity 0.2s; } button.action-btn:active { transform: scale(0.98); }"
)

# 4. Input radius
html = html.replace(
    "input[type=\"number\"], input[type=\"text\"] { width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 4px; font-size: 16px; transition: border-color 0.2s;}",
    "input[type=\"number\"], input[type=\"text\"] { width: 100%; padding: 12px; border: 1px solid var(--border); border-radius: 8px; font-size: 16px; transition: border-color 0.2s, box-shadow 0.2s;}"
)

with open("wos-formula-refiner.html", "w", encoding="utf-8") as f:
    f.write(html)
