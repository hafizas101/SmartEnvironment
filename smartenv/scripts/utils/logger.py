import os

class Logger:
    def __init__(self, base):
        self.base = base

    def log(self, msg):
        print("{}   : {}".format(self.base, msg))


