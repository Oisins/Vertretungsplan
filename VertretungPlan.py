# -*- coding: utf-8 -*-

#
# (c) 2016 Oisín Smith All Rights Reserved
#

import re
import json
from bs4 import BeautifulSoup
from upload import Uploader

OUTPUT_FILE = "vt.json"


def main():
    with open("DI.htm") as file:
        b = BeautifulSoup(file.read(), 'html.parser')

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
            change[1] = change[1].strip()
            changes[key] = change

        if cls not in output.keys():
            output[cls] = []
        output[cls].append(changes)

    with open(OUTPUT_FILE, "w") as file:
        file.write(json.dumps(output))

    Uploader("", OUTPUT_FILE, "")

if __name__ == "__main__":
    main()
