from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from flaskr.forms import AlertForm

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('alerts', __name__)


@bp.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('alert/new.html')


@bp.route('/create', methods=['POST'])
@login_required
def create():
    email = request.form['email']
    title = request.form['title']
    message = request.form['message']
    schedule = request.form['alert-date']
    error = None

    if not email:
        error = 'Title is required.'

    if not message:
        error = 'Message is required.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'INSERT INTO alert (email, message, schedule, title, author_id)'
            ' VALUES (?, ?, ?, ?, ?)',
            (email, message, schedule, title, g.user['id'])
        )
        db.commit()
        return redirect(url_for('alerts.index'))


@bp.route('/')
@login_required
def index():
    db = get_db()
    user_id = session['user_id']
    alerts = db.execute(
        'SELECT a.id, title, schedule, email'
        ' FROM alert a JOIN user u ON a.author_id = u.id'
        f" WHERE a.author_id = {user_id}"
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('alert/index.html', alerts=alerts)
