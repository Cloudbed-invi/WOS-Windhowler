with open("wos-formula-refiner.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "function calcLevel()" in line:
        start_idx = i
        break

if start_idx != -1:
    for i in range(start_idx + 1, len(lines)):
        if "function updateChartZoom()" in line:
            pass # wait
            
    # let's just find the exact block text using Python's string manipulation
    pass

with open("wos-formula-refiner.html", "r", encoding="utf-8") as f:
    code = f.read()

start_sig = "  function calcLevel() {"
end_sig = "function updateChartZoom()"

s_idx = code.find(start_sig)
e_idx = code.find(end_sig)

if s_idx != -1 and e_idx != -1:
    old_block = code[s_idx:e_idx]
    
    new_block = """  function getTierExpectedDamage(level) {
    if (typeof TIER_FORMULAS === 'undefined') return {expected: 0, status: 'Not available'};
    for (const tier of TIER_FORMULAS) {
      if (level >= tier.range[0] && level <= tier.range[1]) {
         const c = tier.coeffs;
         const expected = c[0]*Math.pow(level,3) + c[1]*Math.pow(level,2) + c[2]*level + c[3];
         return {expected: expected, status: tier.provisional ? 'Provisional' : 'Verified'};
      }
    }
    return {expected: 0, status: 'Not available'};
  }

  function calcLevel() {
    const rawVal = document.getElementById('pDmgInput').value.replace(/,/g, '').trim();
    const dmg = parseFloat(rawVal);
    const box = document.getElementById('resLevel');

    if (isNaN(dmg) || dmg <= 0) {
      box.style.display = 'block';
      box.innerHTML = `<div class="result-desc">Please enter a valid damage number.</div>`;
      return;
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
    
    // Power Law Row
    let plStr = (plLvl !== null) ? `Lv. ${plLvl} <span style="font-size:14px;color:var(--text);">at</span> ${(plPct*100).toFixed(1)}%` : 'N/A';
    html += `<div style="display:flex; justify-content:space-between; margin-bottom:12px; align-items:center; font-size:15px;">
               <span style="color:var(--muted);">Global Power-Law:</span>
               <span style="font-weight:600; color:var(--text);">${plStr}</span>
             </div>`;
             
    // Cubic Tier Row
    let cubicStr = (cubicLvl !== null) ? `Lv. ${cubicLvl} <span style="font-size:14px;color:var(--primary);">at</span> ${(cubicPct*100).toFixed(1)}%` : 'Not available';
    let badgeColor = cubicStatus === 'Verified' ? '#4caf50' : (cubicStatus === 'Provisional' ? '#ff9800' : '#9e9e9e');
    let badge = `<span style="font-size:11px; padding:3px 8px; border-radius:12px; background:${badgeColor}; color:white; margin-left:10px; font-weight:600;">${cubicStatus}</span>`;
    
    html += `<div style="display:flex; justify-content:space-between; margin-bottom:8px; align-items:center; border-bottom: 1px solid #eee; padding-bottom: 12px;">
               <div style="font-weight:bold; color:var(--primary); font-size:16px;">Cubic-Tier Match: ${badge}</div>
               <span style="font-weight:bold; font-size:18px; color:var(--primary);">${cubicStr}</span>
             </div>`;
             
    // Difference warning
    if (plLvl !== null && cubicLvl !== null) {
      let diff = Math.abs((cubicLvl + cubicPct) - (plLvl + plPct));
      if (diff > 0.02) {
         html += `<div style="background:#fff3e0; border-left:4px solid #ff9800; padding:12px; font-size:13px; margin-top:12px; color:#d84315; border-radius:4px;">
                    <strong>⚠️ Predictions Differ by >2%:</strong><br>The cubic-tier model and global power-law disagree on this level. 
                    ${cubicStatus === 'Verified' ? 'Trust the <b>Verified</b> Cubic-Tier prediction.' : 'Since the cubic tier is <b>Provisional</b>, both models are uncertain here.'}
                  </div>`;
      }
    } else if (cubicLvl === null && plLvl !== null) {
         html += `<div style="background:#e3f2fd; border-left:4px solid #2196f3; padding:12px; font-size:13px; margin-top:12px; color:#0d47a1; border-radius:4px;">
                    <strong>ℹ️ Extrapolated:</strong> This damage falls outside all known tiers. Falling back to the global power-law approximation.
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
