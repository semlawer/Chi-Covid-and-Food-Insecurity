import re

email = "python peanut@yahoo.com java  panda@gmail.com Thanksgiving henry@uchicago.edu peanutbutter"

# 1
print(re.findall(r'T\w*', email))
print("----")

# 2
s = "1pe2anu3tbu5ttera7nd0je9lly"
x = 0
match = re.findall(r'\d', s)
for i in match:
    x = x+int(i)
print(x)
