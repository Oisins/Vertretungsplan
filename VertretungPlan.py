# -*- coding: utf-8 -*-
#
# (c) 2016 Oisín Smith All Rights Reserved
#

import re
import json
import logging
from bs4 import BeautifulSoup
from upload import Uploader

OUTPUT_FILE = "vt.json"
LOG_FILE = "latest.log"

logging.basicConfig(filename=LOG_FILE,
                    filemode='a',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


def main():
    with open("DI.htm") as file:
        b = BeautifulSoup(file.read(), 'html.parser')

    table = b.find_all("table")[4]

    r = re.compile(r"<h4>(.+?)</h4>.*?\[(.+)\]\s*?--›(?:.*\[(.+)\]|(\s.+)</li>)")

    output = {}

    table = table.find_all("tr")[2:-2]
    for row in table:
        changes = {}
        column = row.td
        sub = str(column.li)
        cls = column.h3.contents[0]

        if cls in ["AG", "1. Semester", "2. Semester", "4. Semester", "4. Semester", "Nachschreiber", "Aufsicht"]:
            continue

        for res in r.findall(sub):
            change = [res[1], (res[2] or res[3]).strip()]
            changes[str(res[0])] = change

        output.setdefault(cls, []).append(changes)

    logging.info("Found " + str(len(table)) + " Items")
    with open(OUTPUT_FILE, "w") as file:
        file.write(json.dumps(output))

    u = Uploader(OUTPUT_FILE, None, "http://www.oisinsmith.eu/Uploader/upload.php")
    u.send_post()

if __name__ == "__main__":
    try:
        logging.info("Program Started")
        main()
        logging.info("Finished\n")
    except BaseException as e:
        logging.error(repr(e))
        raise e
