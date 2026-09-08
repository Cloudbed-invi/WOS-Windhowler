with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

old_fit = """with tab_fit:
    st.subheader("Tier Boundaries & Plot")
    import wos_pipeline
    import matplotlib.pyplot as plt
    import numpy as np"""

new_fit = """with tab_fit:
    st.subheader("Tier Boundaries & Plot")
    import wos_pipeline
    import numpy as np
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        st.warning("matplotlib not installed — install it to see this chart.")
        plt = None"""
code = code.replace(old_fit, new_fit)

# Also need to indent the plot logic under if plt is not None:
old_plot = """    if os.path.exists("data.csv"):
        df = pd.read_csv("data.csv")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(df["Level"] + df["Percent"]/100, df["Damage"], color="blue", label="Raw Data", s=10, alpha=0.5)
        
        for i, tier in enumerate(tiers):
            rng = tier["range"]
            c = tier["coeffs"]
            L_vals = np.linspace(rng[0], rng[1], 100)
            D_vals = c[0]*L_vals**3 + c[1]*L_vals**2 + c[2]*L_vals + c[3]
            color = 'green' if not tier.get("provisional") else 'orange'
            ax.plot(L_vals, D_vals, linewidth=2, color=color, label=f"Tier {i+1} {rng}")
            ax.axvline(rng[1], color='r', linestyle=':', alpha=0.5)
            
        ax.set_yscale('log')
        ax.set_xlabel("Level")
        ax.set_ylabel("Damage (Log Scale)")
        ax.legend()
        st.pyplot(fig)"""

new_plot = """    if os.path.exists("data.csv") and plt is not None:
        df = pd.read_csv("data.csv")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(df["Level"] + df["Percent"]/100, df["Damage"], color="blue", label="Raw Data", s=10, alpha=0.5)
        
        for i, tier in enumerate(tiers):
            rng = tier["range"]
            c = tier["coeffs"]
            L_vals = np.linspace(rng[0], rng[1], 100)
            D_vals = c[0]*L_vals**3 + c[1]*L_vals**2 + c[2]*L_vals + c[3]
            color = 'green' if not tier.get("provisional") else 'orange'
            ax.plot(L_vals, D_vals, linewidth=2, color=color, label=f"Tier {i+1} {rng}")
            ax.axvline(rng[1], color='r', linestyle=':', alpha=0.5)
            
        ax.set_yscale('log')
        ax.set_xlabel("Level")
        ax.set_ylabel("Damage (Log Scale)")
        ax.legend()
        st.pyplot(fig)"""
code = code.replace(old_plot, new_plot)

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)

