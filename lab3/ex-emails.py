import re

f = open("emails.txt", 'r')
text = f.read()
f.close()

matches = re.findall(r'([\w.-]+)(@)(uchicago.edu)', text)
students = []
for i in matches:
    students.append(i[0])

print(students)
