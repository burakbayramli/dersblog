# -*- coding: utf-8 -*-
from flask import Flask
import os

app = Flask(__name__)
        
if __name__ == '__main__':
    app.debug = True
    app.secret_key = "secretkeyverysecret" # needed for session[] to work
    app.run(host="localhost",port=5000)
