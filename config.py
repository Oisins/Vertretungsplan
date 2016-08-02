# -*- coding: utf-8 -*-
import json


class Config:
    def __init__(self, file):
        self.file = file
        self._loaded = False
        self._text = {}

    def load(self):
        try:
            with open(self.file, "r") as file:
                content = file.read()
                if content == "" or content == " ":
                    raise FileNotFoundError
                self._text = json.loads(content)
        except FileNotFoundError:
            self.save()

        self._loaded = True

    def save(self):
        with open(self.file, "w") as f:
            f.write(json.dumps(self._text))

    @property
    def text(self):
        if not self._loaded:
            self.load()
        return self._text

    @text.setter
    def text(self, val):
        self._text = val

    def get(self, item, default=""):
        if item in self.text.keys() and self.text[item] != "":
            return self.text[item]
        return default

    def check(self, *items):
        missing = []
        for i in items:
            if i not in self.text:
                missing.append(i)
                self.text[i] = ""
        self.save()
        return missing
