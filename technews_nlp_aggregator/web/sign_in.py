from . import app

from flask import session, redirect, url_for
@app.route('/sign_in')
def sign_in():
    session["signed_in"] = True
    return redirect(url_for('duplicates'))

@app.route('/sign_out')
def sign_out():
    session["signed_in"] = False
    return redirect(url_for('show_groups'))
