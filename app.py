from flask import Flask, jsonify
app = Flask(__name__)

import requests
import re
from bs4 import BeautifulSoup
import time
import datetime




@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)