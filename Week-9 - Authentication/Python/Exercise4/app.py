#pip install Flask Flask-Bcrypt Flask-SQLAlchemy

from flask import Flask, request, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
import sqlite3
import re
import logging
import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Configure logging for suspicious activities
logging.basicConfig(filename='security.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Database initialization
def init_db():
    with sqlite3.connect('demo.db') as db:
        db.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY, 
                        username TEXT NOT NULL, 
                        password TEXT NOT NULL,
                        login_attempts INTEGER DEFAULT 0,
                        lockout_until TEXT)''')
        db.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', ?)",
                   (bcrypt.generate_password_hash("password123").decode('utf-8'),))

# Check for valid alphanumeric input
def is_valid_input(input_data):
    return bool(re.match("^[a-zA-Z0-9]+$", input_data))

# Function to log suspicious activity
def log_suspicious_activity(username, reason):
    logging.info(f"Suspicious activity detected: User: {username}, Reason: {reason}")

# Function to detect suspicious characters that may indicate an SQL injection attempt
def is_suspicious_input(input_data):
    # SQL Injection pattern detection (checking for suspicious characters like --, ' OR ')
    suspicious_patterns = ["'", "--", " OR ", ";", "="]
    return any(pattern in input_data for pattern in suspicious_patterns)

@app.route('/register', methods=['POST', 'GET'])
def register():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not is_valid_input(username):
            return "Invalid username. Only alphanumeric characters are allowed."

        # Strong password policy
        if password != confirm_password:
            return "Passwords do not match."
        if len(password) < 8 or not any(char.islower() for char in password) or not any(char.isupper() for char in password) \
                or not any(char.isdigit() for char in password) or not any(char in "!@#$%^&*()" for char in password):
            return "Password must be at least 8 characters long, include one uppercase letter, one lowercase letter, one number, and one special character."

        # Hash and salt the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Insert user into database
        with sqlite3.connect('demo.db') as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            db.commit()
        
        message = "Registration successful!"
    return render_template('registration.html', message=message)

@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('demo.db') as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
        
            if user:
                user_id, username, hashed_password, login_attempts, lockout_until = user
                lockout_until = datetime.datetime.strptime(lockout_until, "%Y-%m-%d %H:%M:%S") if lockout_until else None

                # Check if account is locked
                if lockout_until and lockout_until > datetime.datetime.now():
                    message = f"Account locked. Try again after {lockout_until.strftime('%Y-%m-%d %H:%M:%S')}."
                    # Log lockout event
                    log_suspicious_activity(username, "Account locked due to multiple failed attempts")
                    return message
                
                # Verify password
                if bcrypt.check_password_hash(hashed_password, password):
                    # Reset login attempts on successful login
                    cursor.execute("UPDATE users SET login_attempts = 0, lockout_until = NULL WHERE id = ?", (user_id,))
                    db.commit()
                    message = "Login successful!"
                    return redirect(url_for('search'))
                else:
                    # Increment failed login attempts
                    login_attempts += 1
                    if login_attempts >= 3:
                        # Lock account for 5 minutes
                        lockout_until = datetime.datetime.now() + datetime.timedelta(minutes=5)
                        cursor.execute("UPDATE users SET login_attempts = ?, lockout_until = ? WHERE id = ?", 
                                       (login_attempts, lockout_until.strftime("%Y-%m-%d %H:%M:%S"), user_id))
                        db.commit()
                        message = "Account locked due to too many failed attempts. Please try again later."
                        # Log lockout event
                        log_suspicious_activity(username, "Account locked due to multiple failed login attempts")
                    else:
                        cursor.execute("UPDATE users SET login_attempts = ? WHERE id = ?", (login_attempts, user_id))
                        db.commit()
                        message = "Invalid username or password."
                        # Log failed attempt
                        log_suspicious_activity(username, f"Failed login attempt {login_attempts}")
            else:
                message = "Invalid username or password."
                # Log attempt with nonexistent user
                log_suspicious_activity(username, "Login attempt with non-existent username")
    
    return render_template('login.html', message=message)


# Route for the search page (Secured with Parameterized Queries and Read-Only Permissions)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']

        # Check if the input contains suspicious patterns
        if is_suspicious_input(search_query):
            log_suspicious_activity(search_query, "Potential SQL Injection attempt in search query")
            return "Suspicious input detected. Search attempt blocked."

        # Whitelist search input to only allow alphanumeric queries
        if not is_valid_input(search_query):
            return "Invalid search input. Only alphanumeric characters are allowed."
        
        # Open the database in read-only mode (simulating limited DB permissions)
        conn = sqlite3.connect('file:demo.db?mode=ro', uri=True)  # Read-only mode
        cursor = conn.cursor()

        # Secure query using parameterized queries to prevent SQL injection
        query = "SELECT username FROM users WHERE username LIKE ?"
        cursor.execute(query, ('%' + search_query + '%',))
        results = cursor.fetchall()
        conn.close()

        return render_template('search_results.html', results=results)

    return render_template('search.html')

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
