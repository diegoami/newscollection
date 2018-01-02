from . import app

from flask import session, redirect, url_for
@app.route('/sign_in/<string:key>')
def sign_in(key):
    _ = app.application
    if (key == _.db_config["signin_key"]):
        session["signed_in"] = True
    return redirect(url_for('duplicates'))

@app.route('/sign_out')
def sign_out():
    session["signed_in"] = False
    return redirect(url_for('show_groups'))
