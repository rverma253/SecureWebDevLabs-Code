#/system_info?command=whoami; ls

from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
import subprocess

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Initialize the database
def init_db():
    with sqlite3.connect('app.db') as db:
        db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
        db.commit()

# Home page redirects to login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('app.db') as db:
            try:
                db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                db.commit()
                flash("Registration successful! Please log in.")
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash("Username already exists. Try a different one.")
                return redirect(url_for('register'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('app.db') as db:
            user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
            if user:
                session['username'] = username
                return redirect(url_for('upload'))
            else:
                flash("Invalid credentials. Please try again.")
    return render_template('login.html')

# File upload route
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file selected!")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No file selected!")
            return redirect(request.url)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        flash(f"File {file.filename} uploaded successfully.")
    return render_template('upload.html')

# Vulnerable system info route
@app.route('/system_info', methods=['GET'])
def system_info():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Vulnerable: Execute command provided by user
    command = request.args.get('command', 'whoami')
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return render_template('system_info.html', content=result.stdout)

if __name__ == "__main__":
    os.makedirs('uploads', exist_ok=True)
    init_db()
    app.run(debug=True)
