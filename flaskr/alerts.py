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


def get_alert(id):
    alert = get_db().execute(
        'SELECT a.id, title, message, email, schedule'
        ' FROM alert a'
        ' WHERE a.id = ?',
        (id,)
    ).fetchone()

    if alert is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return alert


@bp.route('/<int:id>/edit', methods=['GET'])
@login_required
def edit(id):
    alert = get_alert(id)
    return render_template('alert/edit.html', alert=alert)


@bp.route('/<int:id>/update', methods=['POST'])
@login_required
def update(id):

    title = request.form['title']
    message = request.form['message']
    email = request.form['email']
    schedule = request.form['schedule']
    error = None

    if not title:
        error = 'Title is required.'

    if not email:
        error = 'Email is required.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'UPDATE alert SET title = ?, message= ?, email= ?, schedule= ?'
            ' WHERE id = ?',
            (title, message, email, schedule, id)
        )
        db.commit()
        return redirect(url_for('alerts.index'))