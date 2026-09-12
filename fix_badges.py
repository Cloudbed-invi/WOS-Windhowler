with open("wos-formula-refiner.html", "r", encoding="utf-8") as f:
    html = f.read()

old_badge_logic = """    let exactBadge = '';
    if (exactExtrapolated) {
        exactBadge = `<span style="font-size:11px; padding:3px 8px; border-radius:12px; background:#9e9e9e; color:white; margin-left:10px; font-weight:600;">Extrapolated</span>`;
    } else if (exactConfirmed) {
        exactBadge = `<span style="font-size:11px; padding:3px 8px; border-radius:12px; background:#4caf50; color:white; margin-left:10px; font-weight:600;">Verified (Huber)</span>`;
    } else {
        exactBadge = `<span style="font-size:11px; padding:3px 8px; border-radius:12px; background:#2196f3; color:white; margin-left:10px; font-weight:600;">Interpolated</span>`;
    }"""

new_badge_logic = """    let exactBadge = '';
    if (exactExtrapolated) {
        exactBadge = `<span class="badge badge-extrapolated" style="margin-left:10px;">Extrapolated</span>`;
    } else if (exact.clustered) {
        exactBadge = `<span class="badge badge-extrapolated" style="margin-left:10px;">Provisional (Clustered)</span>`;
    } else if (exactConfirmed) {
        exactBadge = `<span class="badge badge-verified" style="margin-left:10px;">Verified (Huber)</span>`;
    } else {
        exactBadge = `<span class="badge badge-interpolated" style="margin-left:10px;">Interpolated</span>`;
    }"""

html = html.replace(old_badge_logic, new_badge_logic)

with open("wos-formula-refiner.html", "w", encoding="utf-8") as f:
    f.write(html)
