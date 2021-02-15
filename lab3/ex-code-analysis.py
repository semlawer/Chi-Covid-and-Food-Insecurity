import re

f = open("play.py", 'r')
text = f.read()
f.close()
print(re.findall(r"([\t ]*def \w+\(.*\))", text))
