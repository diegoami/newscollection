from . import app
from flask import request, render_template, session

from flask import render_template,  request
@app.route('/sign_in')
def sign_in():
    session["signed_in"] = True
    return render_template('home.html')

@app.route('/sign_out')
def sign_out():
    session["signed_in"] = False
    return render_template('home.html')
