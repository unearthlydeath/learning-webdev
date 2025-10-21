from flask import Flask, render_template, request, redirect, url_for, session
import os, json


# initializations
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')

# simple file to store username/password pairs for this demo
USERS_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'users.json')


def load_users():
    """Load users from USERS_FILE. Returns dict username->password."""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f)


# ROUTES


@app.route('/')
def index():
    return render_template('landing.html', username=session.get('username'), active='landing')


@app.route('/about')
def about_page():
    return render_template('about.html', username=session.get('username'), active='about')


@app.route('/home')
def home_page():
    # If the user is not logged in, render the home template with a flag
    # that instructs the page to show a login call-to-action instead of
    # personal content. This keeps the URL at /home but requires login
    # to access user-specific data.
    username = session.get('username')
    requires_login = username is None
    return render_template('home.html', username=username, active='home', requires_login=requires_login)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        users = load_users()
        # simple credential check (plaintext) for demo purposes
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home_page'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error, username=session.get('username'), active='login')


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            error = 'Both username and password are required.'
        else:
            users = load_users()
            if username in users:
                error = 'That username is already taken.'
            else:
                users[username] = password
                save_users(users)
                # automatically log the user in after signup
                session['username'] = username
                return redirect(url_for('home_page'))
    return render_template('signup.html', error=error, username=session.get('username'), active='signup')


@app.route('/logout')
def logout_page():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/settings')
def settings_page():
    # simple placeholder page for settings
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('settings.html', username=session.get('username'), active='settings')


if (__name__ == '__main__'):
    app.run(debug=True)
