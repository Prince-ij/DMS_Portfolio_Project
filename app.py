#!/usr/bin/python3
from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

@app.route('/')
def hello():
    return 'hello world'

if __name__ == '__main__':
    app.run()
