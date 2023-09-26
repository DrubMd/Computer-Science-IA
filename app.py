from flask import Flask, render_template, request, redirect, url_for, flash, abort

import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjfnjewfjejwejjf'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_flashcard(flashcard_id):
    conn = get_db_connection()
    flashcard = conn.execute('SELECT * FROM flashcards WHERE id = ?',
                        (flashcard_id,)).fetchone()
    conn.close()
    if flashcard is None:
        abort(404)
    return flashcard

@app.route('/')
def index():
    conn = get_db_connection()
    flashcards = conn.execute('SELECT * FROM flashcards').fetchall()
    conn.close()
    return render_template('index.html', flashcards=flashcards)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        term = request.form['term']
        defenition = request.form['defenition']

        if not term:
            flash('Term is required!')
        elif not defenition:
            flash('defenition is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO flashcards (term, defenition) VALUES (?, ?)',
                         (term, defenition))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    return render_template('create.html')

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    flashcard = get_flashcard(id)

    if request.method == 'POST':
        term = request.form['term']
        defenition = request.form['defenition']

        if not term:
            flash('Term is required!')

        elif not defenition:
            flash('Definition is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE flashcards SET term = ?, defenition = ?'
                         ' WHERE id = ?',
                         (term, defenition, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', flashcard=flashcard)

if __name__ == '__main__':
    app.run(debug=True)