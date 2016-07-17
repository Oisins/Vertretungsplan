# -*- coding: utf-8 -*-

#
# (c) 2016 Oisín Smith All Rights Reserved
#

import requests
import os


class Uploader:
    def __init__(self, filename, filedir, url):
        """
        Init All Variables
        :param filename: Name of File to be uploaded
        :param filedir: Directory in which the File is located
        ;param url: Url the file will be sent to
        :return:
        """
        self.fileName = filename
        self.fileDir = filedir
        self.url = url

    def send_post(self):
        """
        Take Staged File und send POST request
        :return:
        """
        if self.fileDir:
            os.chdir(self.fileDir)

        files = {'file': open(self.fileName, "rb")}
        req = requests.post(self.url, files=files)

        return req.status_code == requests.codes.ok
