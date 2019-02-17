from flask import Flask
from application import database, crawler

app = Flask(__name__)
app.config.from_object(__name__)
