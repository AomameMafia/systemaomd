from flask import Flask
from flask import request
from threading import Thread
import time
import requests
import random

app = Flask('')

@app.route('/')
def home():
  return "работаем братья!"

def run():
  app.run(host='0.0.0.0', port = random.randint(200,900))

def phone_al():
  t = Thread(target=run)
  t.start()