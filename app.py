from flask import Flask,request
from config import Configuration

app = Flask(__name__,static_folder="static")
app.config.from_object(Configuration)