import re

with open("wos-formula-refiner.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Dark Theme Variables and UI enhancements
css_injection = """
  :root[data-theme="dark"] {
    --bg: #121212;
    --card: #1e1e1e;
    --text: #e0e0e0;
    --muted: #a0a0a0;
    --primary: #4dabf7;
    --border: #333333;
    --success: #40c057;
    --warning: #fa5252;
  }
  
  /* Smooth transitions for theme toggle */
  body, .card, input, button, .result-box, .tab-btn {
    transition: background-color 0.3s, color 0.3s, border-color 0.3s;
  }
  
  /* Mobile optimized tabs */
  .tabs { 
    display: flex; 
    gap: 8px; 
    margin-bottom: 20px; 
    overflow-x: auto; 
    white-space: nowrap; 
    -webkit-overflow-scrolling: touch; 
    padding-bottom: 5px; 
    justify-content: flex-start; 
  }
  /* Hide scrollbar for tabs */
  .tabs::-webkit-scrollbar { display: none; }
  .tabs { -ms-overflow-style: none; scrollbar-width: none; }
  
  .tab-btn { flex-shrink: 0; }
  
  /* Theme Toggle Button */
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
  }
  
  /* Inputs */
  input[type="number"], input[type="text"] {
    background-color: var(--card);
    color: var(--text);
  }
  input:focus {
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.25);
  }
  
  /* Result box dark mode fixes */
  :root[data-theme="dark"] .result-box {
    background-color: #1a252f;
    border-color: #2c3e50;
  }
  
  :root[data-theme="dark"] .unconfirmed-bg {
    background-color: #2a1a1a;
  }
  
  :root[data-theme="dark"] .formula-banner {
    background-color: #2b2510;
    border-color: #f39c12;
  }
  
  @media (min-width: 600px) {
    .tabs { justify-content: center; }
  }
"""

html = html.replace("    .tabs { display: flex; gap: 10px; margin-bottom: 20px; justify-content: center; }", css_injection)

# 2. Inject Theme Toggle Button
btn_html = """
<body>
<button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle Dark Mode">🌙</button>
"""
html = html.replace("<body>", btn_html)

# 3. Inject JS for Dark Mode
js_injection = """
  // Dark Mode Toggle Logic
  function toggleTheme() {
    const root = document.documentElement;
    const isDark = root.getAttribute('data-theme') === 'dark';
    const newTheme = isDark ? 'light' : 'dark';
    root.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    document.querySelector('.theme-toggle').textContent = newTheme === 'dark' ? '☀️' : '🌙';
  }
  
  // Set initial theme
  document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.querySelector('.theme-toggle').textContent = savedTheme === 'dark' ? '☀️' : '🌙';
  });

"""
html = html.replace("<script>", "<script>\n" + js_injection)

with open("wos-formula-refiner.html", "w", encoding="utf-8") as f:
    f.write(html)
