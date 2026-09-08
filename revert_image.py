with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("st.image(img_dict[\"data\"], width='stretch')", "st.image(img_dict[\"data\"], use_container_width=True)")

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)
