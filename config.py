# -*- coding: utf-8 -*-
import os
import json


class Config:
    def __init__(self, file):
        self.file = file
        self.loaded = False
        self.text = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                a = f.read()
                self.text = json.loads(a)
        else:
            self.save()

        self.loaded = True

    def save(self):
        with open(self.file, "w") as f:
            f.write(json.dumps(self.text))

    def get(self, item, default=""):
        if not self.loaded:
            self.load()
        try:
            if self.text[item] == "":
                raise KeyError
            return self.text[item]
        except KeyError:
            return default

    def check(self, items):
        missing = []
        for i in items:
            if i not in self.text:
                missing.append(i)
                self.text[i] = ""
        self.save()
        return missing
