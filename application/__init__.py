from flask import Flask
from application import database, crawler

app = Flask(__name__)
# app.secret_key = 'hello_world'
app.config.from_object(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///immeubles.db'
