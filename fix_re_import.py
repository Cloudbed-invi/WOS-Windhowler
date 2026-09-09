with open("wos_pipeline.py", "r", encoding="utf-8") as f:
    code = f.read()

# Fix UnboundLocalError by importing re globally or before it's used
# I'll just replace "import cv2" with "import cv2\nimport re" at the top of the file.
if "import cv2\nimport re" not in code:
    code = code.replace("import cv2", "import cv2\nimport re")
    
# And remove the internal try/import re
code = code.replace("        try:\n            import re", "        try:")

with open("wos_pipeline.py", "w", encoding="utf-8") as f:
    f.write(code)
