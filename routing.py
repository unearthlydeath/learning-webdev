#imports
from flask import Flask, send_from_directory, send_file, request, jsonify
import os, json


#initalizations
app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
def serve_html(name):
    """Serve a file as text/html. If an extensionless file is present (like 'main_page'),
    serve it with the text/html mimetype so browsers render it instead of downloading.
    If a file with the same name plus '.html' exists, prefer that.
    """
    # try the exact filename first
    path = os.path.join(base_dir, name)
    if not os.path.exists(path):
        # try with .html extension
        alt = path + '.html'
        if os.path.exists(alt):
            path = alt
        else:
            # fallback to send_from_directory which will return a 404 if missing
            return send_from_directory(base_dir, name)

    # serve with explicit mimetype so the browser won't download it
    return send_file(path, mimetype='text/html')

#main code

@app.route('/notaker')
def index():
    return serve_html('landing')

@app.route('/about')
def about_page():
    return serve_html('about')

@app.route('/home')
def home_page():
    return serve_html('home')

@app.route('/login')
def login_page():
    return serve_html('login')


#run server
if (__name__ == '__main__'):
    app.run(debug=True)