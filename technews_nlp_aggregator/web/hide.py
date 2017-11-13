
from . import app
from flask import request, render_template, session, redirect, url_for

from flask import render_template,  request
@app.route('/hide/<int:article_id>')
def hide(article_id):
    return redirect(url_for('browse'))
