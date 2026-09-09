import re
damage_str = "102 067 675 "
print(int(re.sub(r'[^\d]', '', damage_str)))
