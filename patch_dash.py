with open("admin_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

old_loop = """            for lvl in levels:
                d = df_data[df_data["Level"] == lvl]
                count = len(d)
                conf = round(d["Confidence"].mean(), 3) if (has_conf and count > 0 and not d["Confidence"].isna().all()) else None
                cov_rows.append({"Level": lvl, "Confirmed Points": count, "Avg Confidence": conf})

            df_cov = pd.DataFrame(cov_rows)
            def highlight_low(row):
                color = 'background-color: #ffcccc; color: #900' if row['Confirmed Points'] < 3 else ''
                return [color]*len(row)"""

new_loop = """            for lvl in levels:
                d = df_data[df_data["Level"] == lvl]
                count = len(d)
                conf = round(d["Confidence"].mean(), 3) if (has_conf and count > 0 and not d["Confidence"].isna().all()) else None
                
                status = "No Data"
                spread = 0.0
                if count > 0:
                    unique_pcts = d["Percent"].nunique()
                    if unique_pcts < 2:
                        status = "Unverifiable (Need >1 pt)"
                    else:
                        spread = d["Percent"].max() - d["Percent"].min()
                        if spread >= 25.0:
                            status = "Verified (Strong)"
                        else:
                            status = "Provisional (Clustered)"
                            
                cov_rows.append({
                    "Level": lvl, 
                    "Status": status,
                    "Spread (%)": f"{spread:.1f}%" if count > 1 else "-",
                    "Confirmed Points": count, 
                    "Avg Confidence": conf
                })

            df_cov = pd.DataFrame(cov_rows)
            def highlight_low(row):
                if row['Status'] == 'No Data' or row['Status'].startswith('Unverifiable'):
                    color = 'background-color: #ffcccc; color: #900'
                elif row['Status'] == 'Provisional (Clustered)':
                    color = 'background-color: #fff3cd; color: #856404'
                elif row['Status'] == 'Verified (Strong)':
                    color = 'background-color: #d4edda; color: #155724'
                else:
                    color = ''
                return [color]*len(row)"""

code = code.replace(old_loop, new_loop)

with open("admin_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)
