with open("wos-formula-refiner.html", "r", encoding="utf-8") as f:
    html = f.read()

# CSS Badge Classes
badge_css = """
  .badge { padding: 3px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; }
  .badge-verified { background: #d4edda; color: #155724; }
  .badge-interpolated { background: #e2e3e5; color: #383d41; }
  .badge-extrapolated { background: #fff3cd; color: #856404; }
  .badge-not-available { background: #f8d7da; color: #721c24; }
  
  :root[data-theme="dark"] .badge-verified { background: #1a4a2b; color: #8ee0a3; }
  :root[data-theme="dark"] .badge-interpolated { background: #2d3748; color: #a0aec0; }
  :root[data-theme="dark"] .badge-extrapolated { background: #5c4309; color: #f6e05e; }
  :root[data-theme="dark"] .badge-not-available { background: #631c23; color: #fca5a5; }
  
  .tab-btn:hover { background: var(--border); color: var(--text); }
  .tab-btn.active:hover { background: var(--primary); color: white; }
  .tab-btn:active { transform: scale(0.96); }
"""

html = html.replace("</style>", badge_css + "\n</style>")

# Replace JS badge definitions
old_badges = """    const badges = {
      "Verified": `<span style="background:#d4edda; color:#155724; padding:3px 8px; border-radius:12px; font-size:12px;">Verified</span>`,
      "Interpolated": `<span style="background:#e2e3e5; color:#383d41; padding:3px 8px; border-radius:12px; font-size:12px;">Interpolated</span>`,
      "Extrapolated": `<span style="background:#fff3cd; color:#856404; padding:3px 8px; border-radius:12px; font-size:12px;">Extrapolated</span>`,
      "Not Available": `<span style="background:#f8d7da; color:#721c24; padding:3px 8px; border-radius:12px; font-size:12px;">Not Available</span>`
    };"""

new_badges = """    const badges = {
      "Verified": `<span class="badge badge-verified">Verified</span>`,
      "Interpolated": `<span class="badge badge-interpolated">Interpolated</span>`,
      "Extrapolated": `<span class="badge badge-extrapolated">Extrapolated</span>`,
      "Not Available": `<span class="badge badge-not-available">Not Available</span>`
    };"""

html = html.replace(old_badges, new_badges)

with open("wos-formula-refiner.html", "w", encoding="utf-8") as f:
    f.write(html)
