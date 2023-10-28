from flask import Flask, render_template, request, redirect, url_for, flash, abort, Response, session
import sqlite3
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user, login_manager
from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.secret_key = 'rcctufiygugugy'

login_manager = LoginManager(app)
login_manager.login_view = "login"
class User(UserMixin):
    def __init__(self, id, username, password):
         self.id = str(id)
         self.username = username
         self.password = password
         self.authenticated = False
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id



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


@login_manager.user_loader
def load_user(user_id):
   conn = get_db_connection()
   curs = conn.cursor()
   curs.execute("SELECT * from users where user_id = (?)",[user_id])
   user_data = curs.fetchone()
   if user_data is None:
    return None
   else:
    user = User(user_data['user_id'], user_data['username'], user_data['password'])
    return user
   
@app.route('/')
@login_required
def index():
    user_id = current_user.id
    conn = get_db_connection()
    flashcards = conn.execute('SELECT * FROM flashcards WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return render_template('index.html', flashcards=flashcards, user_id=user_id)

@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
     return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
     conn = get_db_connection()
     curs = conn.cursor()
     curs.execute("SELECT * FROM users where username = (?)",    [form.username.data])
     user = list(curs.fetchone())
     Us = load_user(user[0])
     if form.username.data == Us.username and form.password.data == Us.password:
        login_user(Us, remember=form.remember.data)
        Uname = list({form.username.data})[0].split('@')[0]
        flash('Logged in successfully '+Uname)
        redirect(url_for('index'))
     else:
        flash('Login Unsuccessfull.')
  return render_template('login.html',title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        curs = conn.cursor()
        curs.execute("SELECT * FROM users WHERE username = ?", [form.username.data])
        user = curs.fetchone()

        if user:
            flash('Registration failed. This username is already taken.', 'error')
        else:
            curs.execute("INSERT INTO users (username, password) VALUES (?, ?)", (form.username.data, form.password.data))
            conn.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)
    
@app.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        term = request.form['term']
        definition = request.form['definition']

        if not term:
            flash('Term is required!')
        elif not definition:
            flash('definition is required!')
        else:
            user_id = current_user.id  # Get the user's ID from the current_user
            conn = get_db_connection()
            conn.execute('INSERT INTO flashcards (user_id,term, definition) VALUES (?, ?, ?)',
                         (user_id, term, definition))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    return render_template('create.html')

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
@login_required
def edit(id):
    flashcard = get_flashcard(id)

    if request.method == 'POST':
        term = request.form['term']
        definition = request.form['definition']

        if not term:
            flash('Term is required!')

        elif not definition:
            flash('Definition is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE flashcards SET term = ?, definition = ?'
                         ' WHERE id = ?',
                         (term, definition, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', flashcard=flashcard)

if __name__ == '__main__':
    app.run(debug=True)