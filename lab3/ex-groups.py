import re


def find_funcs(filenames):
    funcs = []
    for filename in filenames:
        g = open(filename, 'r')
        text = g.read()
        g.close()
        matches = re.findall(r'(def )(\w+)(\()(\w+)(\))()', text)
        for i in matches:
            funcs.append(i[1]+"," + filename)
            funcs.sort()
    return funcs


funcs = find_funcs(["play.py", "plot_lab.py"])
for tup in funcs:
    print(tup)
