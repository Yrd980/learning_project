from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from setting import BaseConfig

app = Flask("library")

CORS(app, resources=r"/*")

app.config.from_object(BaseConfig)

db = SQLAlchemy(app)
