from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bryophyta.auth import login_required
from bryophyta.db import get_db
from bryophyta.logic.document import Document
from bryophyta.logic.dropbox import Dropbox

bp = Blueprint('dropbox', __name__)


@bp.route('/')
def index():
    db = get_db()
    documents = db.execute(
        'SELECT d.id, title, body, created, author_id, username'
        ' FROM document d JOIN user u ON d.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('dropbox/index.html', documents=documents)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO document (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('dropbox.index'))

    return render_template('dropbox/create.html')

def get_document(id, check_author=True):
    document = get_db().execute(
        'SELECT d.id, title, body, created, author_id, username, percent_match'
        ' FROM document d JOIN user u ON d.author_id = u.id'
        ' WHERE d.id = ?',
        (id,)
    ).fetchone()

    if document is None:
        abort(404, f"Document id {id} doesn't exist.")

    if check_author and document['author_id'] != g.user['id']:
        abort(403)

    return document


def get_documents(id, check_author=True):

    return documents


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    document = get_document(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE document SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('dropbox.index'))

    return render_template('dropbox/update.html', document=document)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_document(id)
    db = get_db()
    db.execute('DELETE FROM document WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('dropbox.index'))


@bp.route('/calculate', methods=('GET', 'POST'))
@login_required
def calculate():
    if request.method == 'POST':
        return redirect(url_for('dropbox.index'))

    db = get_db()
    documents = db.execute(
        'SELECT d.id, title, body, created, author_id, username'
        ' FROM document d JOIN user u ON d.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    docs = [Document(d['id'], d['title'], d['body']) for d in documents]
    dropbox = Dropbox(docs)
    dropbox.calculate()
    documents = dropbox.documents
    matches = dropbox.list_matches()

    return render_template('dropbox/report.html', documents=documents, matches=matches)
