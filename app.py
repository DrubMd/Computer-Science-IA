from flask import Flask, render_template, request, redirect, url_for, flash, abort
import sqlite3
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command
from user import User

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


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
    if current_user.is_authenticated:
        conn = get_db_connection()
        flashcards = conn.execute('SELECT * FROM flashcards').fetchall()
        conn.close()
        return render_template('index.html', flashcards=flashcards)
    else:
        return '<a class="button" href="/login">Google Login</a>'
    
@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

# Find out what URL to hit to get tokens that allow you to ask for
# things on behalf of a user
google_provider_cfg = get_google_provider_cfg()
token_endpoint = google_provider_cfg["token_endpoint"]

# Prepare and send a request to get tokens! Yay tokens!
token_url, headers, body = client.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url=request.base_url,
    code=code
)
token_response = requests.post(
    token_url,
    headers=headers,
    data=body,
    auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
)

# Parse the tokens!
client.parse_request_body_response(json.dumps(token_response.json()))

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        term = request.form['term']
        definition = request.form['definition']

        if not term:
            flash('Term is required!')
        elif not definition:
            flash('definition is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO flashcards (term, definition) VALUES (?, ?)',
                         (term, definition))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    return render_template('create.html')

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
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