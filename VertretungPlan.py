# -*- coding: utf-8 -*-
#
# (c) 2016 Oisín Smith All Rights Reserved
#
import re
import json
import logging
import os
import locale
from datetime import datetime, date
from bs4 import BeautifulSoup
from upload import Uploader


OUTPUT_FILE = "vt.json"
LOG_FILE = "latest.log"
UPLOAD_URL = "http://www.oisinsmith.eu/Uploader/upload.php"

logging.basicConfig(filename=LOG_FILE,
                    filemode='a',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


def main():
    locale.setlocale(locale.LC_ALL, '')  # Set Locale to german
    logging.debug("Localization is {}".format(locale.getlocale()[0]))

    files = [file for file in os.listdir(".") if file.endswith(".htm")]  # List all files ending with .htm
    files.sort(key=lambda x: os.path.getmtime(x))  # Get the newest file
    latest_file = files[-1]

    logging.info("Latest File is %s" % latest_file)

    with open(latest_file) as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

    table_soup = soup.find_all("table")[4]
    table = table_soup.find_all("tr")[2:-2]

    date_for_soup = soup.find_all("h2")[0].contents[0]
    print(date_for_soup)
    date_for = re.search(r"Vertretungsplan für Freitag (\d\d\. \w+ \d\d\d\d)", date_for_soup).group(1)

    date_created_soup = soup.find_all("h3")[0].contents[0]
    date_created_re = re.search(r"erstellt am (\d\d\. \w+)\W*(\d\d\d\d) um (\d\d:\d\d) Uhr", date_created_soup)
    date_created = " ".join(date_created_re.groups())  # Join regex to DAY MONTH YEAR HOUR MINUTE

    datetime_created = datetime.strptime(date_created, "%d. %B %Y %H:%M")
    datetime_for = datetime.strptime(date_for, "%d. %B %Y")

    r = re.compile(r"<h4>(.+?)</h4>.*?\[(.+)\]\s*?--›(?:.*\[(.+)\]|(\s.+)</li>)")  # Regex all substitutions

    output = {}

    for row in table:
        changes = {}
        column = row.td
        sub = str(column.li)
        cls = column.h3.contents[0]  # Current Class

        if cls in ["AG", "1. Semester", "2. Semester", "4. Semester", "4. Semester", "Nachschreiber", "Aufsicht"]:
            continue  # Skip non supported substitutions

        for res in r.findall(sub):
            change = [res[1], (res[2] or res[3]).strip()]  # Accept both substitution formats
            changes[str(res[0])] = change

        output.setdefault(cls, []).append(changes)  # Append to output. If list doesn't exist create new

    logging.info("Found " + str(len(table)) + " Item(s)")

    output = {"date": str(datetime_for), "created": str(datetime_created), "data": output}
    with open(OUTPUT_FILE, "w") as file:
        file.write(json.dumps(output))

    u = Uploader(OUTPUT_FILE, None, UPLOAD_URL)
    u.send_post()

if __name__ == "__main__":
    try:
        logging.info("Program Started")
        main()
        logging.info("Finished\n")
    except Exception as e:
        logging.exception("Exception")
        raise e
