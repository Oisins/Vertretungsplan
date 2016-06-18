# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import json


with open("DI.htm") as file:
    f = file.read()

b = BeautifulSoup(f, 'html.parser')

table = b.find_all("table")[4]

r = re.compile(r"<h4>(.+?)</h4>.*?\[(.+)\]\s*?--›(?:.*\[(.+)\]|(\s.+)</li>)")

output = {}

for row in table.find_all("tr")[2:-2]:
    changes = {}
    column = row.td
    sub = str(column.li)
    cls = column.h3.contents[0]

    if cls in ["AG"]:
        continue
    # print("Class: " + str(cls))

    for res in r.findall(sub):
        key = str(res[0])

        change = [res[1], res[2] or res[3]]
        changes[key] = change

    if cls not in output.keys():
        output[cls] = []
    output[cls].append(changes)

with open("vt.json", "w") as file:
    file.write(json.dumps(output))
