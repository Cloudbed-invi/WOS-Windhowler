import re

with open("wos-formula-refiner.html", "r", encoding="utf-8") as f:
    code = f.read()

# Replace calcLevel block
start_sig = "  function calcLevel() {"
end_sig = "  function updateChartZoom() {"

s_idx = code.find(start_sig)
e_idx = code.find(end_sig)

if s_idx != -1 and e_idx != -1:
    new_block = """  function calcLevel() {
    const rawVal = document.getElementById('pDmgInput').value.replace(/,/g, '').trim();
    const dmg = parseFloat(rawVal);
    const box = document.getElementById('resLevel');

    if (isNaN(dmg) || dmg <= 0) {
      box.style.display = 'block';
      box.innerHTML = `<div class="result-desc">Please enter a valid damage number.</div>`;
      return;
    }

    // 0. Exact ML Data (Old Model - Huber / Interpolated)
    let exactLvl = null, exactPct = null, exactConfirmed = false, exactExtrapolated = false;
    if (typeof EXACT_LEVELS !== 'undefined') {
      const sortedKeys = Object.keys(EXACT_LEVELS).map(Number).sort((a,b)=>a-b);
      for (const lvl of sortedKeys) {
        const data = EXACT_LEVELS[lvl];
        const end = data.start + data.window;
        if (dmg >= data.start && dmg <= end) {
          exactLvl = lvl;
          exactPct = (dmg - data.start) / data.window;
          exactConfirmed = data.confirmed;
          if (data.extrapolated) exactExtrapolated = true;
          break;
        }
      }
    }

    // 1. Power-Law Prediction (Global Fallback)
    let plLvl = null, plPct = null;
    if (typeof EXTRAPOLATE_A !== 'undefined' && typeof EXTRAPOLATE_B !== 'undefined') {
      const approxLevelFloat = Math.pow(dmg / EXTRAPOLATE_A, 1 / EXTRAPOLATE_B);
      plLvl = Math.floor(approxLevelFloat);
      const plStart = EXTRAPOLATE_A * Math.pow(plLvl, EXTRAPOLATE_B);
      const plNext = EXTRAPOLATE_A * Math.pow(plLvl + 1, EXTRAPOLATE_B);
      plPct = (dmg - plStart) / (plNext - plStart);
    }

    // 2. Cubic-Tier Prediction
    let cubicLvl = null, cubicPct = null, cubicStatus = 'Not available';
    for (let L = 1; L <= 150; L++) {
      let current = getTierExpectedDamage(L);
      let next = getTierExpectedDamage(L + 1);
      
      if (current.status !== 'Not available' && next.status !== 'Not available') {
        if (dmg >= current.expected && dmg < next.expected) {
          cubicLvl = L;
          cubicPct = (dmg - current.expected) / (next.expected - current.expected);
          cubicStatus = current.status;
          break;
        }
      }
    }

    // Build UI
    box.style.display = 'block';
    let html = '';
    
    // Exact ML Row
    let exactStr = (exactLvl !== null) ? `Lv. ${exactLvl} <span style="font-size:14px;color:var(--text);">at</span> ${(exactPct*100).toFixed(1)}%` : 'Not available';
    let exactBadge = '';
    if (exactExtrapolated) {
        exactBadge = `<span style="font-size:11px; padding:3px 8px; border-radius:12px; background:#9e9e9e; color:white; margin-left:10px; font-weight:600;">Extrapolated</span>`;
    } else if (exactConfirmed) {
        exactBadge = `<span style="font-size:11px; padding:3px 8px; border-radius:12px; background:#4caf50; color:white; margin-left:10px; font-weight:600;">Verified (Huber)</span>`;
    } else {
        exactBadge = `<span style="font-size:11px; padding:3px 8px; border-radius:12px; background:#2196f3; color:white; margin-left:10px; font-weight:600;">Interpolated</span>`;
    }
    
    html += `<div style="display:flex; justify-content:space-between; margin-bottom:12px; align-items:center; font-size:16px; border-bottom: 2px solid #eee; padding-bottom: 12px;">
               <div style="font-weight:bold; color:var(--text);">Old ML Model: ${exactBadge}</div>
               <span style="font-weight:bold; font-size:18px; color:var(--text);">${exactStr}</span>
             </div>`;
             
    // Cubic Tier Row
    let cubicStr = (cubicLvl !== null) ? `Lv. ${cubicLvl} <span style="font-size:14px;color:var(--primary);">at</span> ${(cubicPct*100).toFixed(1)}%` : 'Not available';
    let badgeColor = cubicStatus === 'Verified' ? '#4caf50' : (cubicStatus === 'Provisional' ? '#ff9800' : '#9e9e9e');
    let badge = `<span style="font-size:11px; padding:3px 8px; border-radius:12px; background:${badgeColor}; color:white; margin-left:10px; font-weight:600;">${cubicStatus}</span>`;
    
    html += `<div style="display:flex; justify-content:space-between; margin-bottom:12px; align-items:center; padding-top: 4px;">
               <div style="font-weight:bold; color:var(--primary); font-size:15px;">Cubic-Tier Match: ${badge}</div>
               <span style="font-weight:bold; font-size:16px; color:var(--primary);">${cubicStr}</span>
             </div>`;

    // Power Law Row
    let plStr = (plLvl !== null) ? `Lv. ${plLvl} <span style="font-size:14px;color:var(--text);">at</span> ${(plPct*100).toFixed(1)}%` : 'N/A';
    html += `<div style="display:flex; justify-content:space-between; margin-bottom:12px; align-items:center; font-size:14px;">
               <span style="color:var(--muted); font-weight:600;">Global Power-Law:</span>
               <span style="font-weight:600; color:var(--muted);">${plStr}</span>
             </div>`;
             
    // Difference warning
    if (plLvl !== null && cubicLvl !== null) {
      let diff = Math.abs((cubicLvl + cubicPct) - (plLvl + plPct));
      if (diff > 0.02) {
         html += `<div style="background:#fff3e0; border-left:4px solid #ff9800; padding:12px; font-size:13px; margin-top:12px; color:#d84315; border-radius:4px;">
                    <strong>⚠️ Curve Predictions Differ by >2%:</strong><br>The cubic-tier curve and global power-law curve diverge heavily here. 
                    ${cubicStatus === 'Verified' ? 'Trust the <b>Verified</b> Cubic-Tier prediction.' : 'Since the cubic tier is <b>Provisional</b>, rely on the Old ML Model (Huber) if available.'}
                  </div>`;
      }
    } else if (cubicLvl === null && plLvl !== null) {
         html += `<div style="background:#e3f2fd; border-left:4px solid #2196f3; padding:12px; font-size:13px; margin-top:12px; color:#0d47a1; border-radius:4px;">
                    <strong>ℹ️ Extrapolated:</strong> This damage falls outside all known tiers. Falling back to the global power-law curve approximation.
                  </div>`;
    }
    
    html += `<div style="margin-top: 15px; padding-top: 10px; font-size: 13px; text-align: center;">
            Data looks inaccurate? <a href="https://forms.gle/CKsANz8zpjNJWFN46" target="_blank" style="color: var(--primary); font-weight: bold; text-decoration: none;">Submit your real damage to help train the AI!</a>
          </div>`;
          
    box.innerHTML = html;
  }

"""
    code = code[:s_idx] + new_block + code[e_idx:]
    with open("wos-formula-refiner.html", "w", encoding="utf-8") as f:
        f.write(code)
