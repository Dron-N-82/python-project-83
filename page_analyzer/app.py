import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

'''
@app.route("/")
def hello():
    return "Welcome to Flask!"
'''

@app.route("/")
def home_page():
    return render_template('index.html')