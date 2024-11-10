from flask import Flask, request, render_template_string, render_template, redirect, url_for
import sqlite3
import re
import logging

app = Flask(__name__)

# Configure logging to log all suspicious activities
logging.basicConfig(filename='security.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize the database and insert sample data
def init_db():
    with sqlite3.connect('demo.db') as db:
        db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)')
        db.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'password123')")
        db.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('bob', 'bobpass')")
        db.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('alice', 'alicepass')")

# Whitelist function to allow only alphanumeric characters in usernames and passwords
def is_valid_input(input_data):
    return bool(re.match("^[a-zA-Z0-9]+$", input_data))

# Function to detect suspicious characters that may indicate an SQL injection attempt
def is_suspicious_input(input_data):
    # SQL Injection pattern detection (checking for suspicious characters like --, ' OR ')
    suspicious_patterns = ["'", "--", " OR ", ";", "="]
    return any(pattern in input_data for pattern in suspicious_patterns)

# Log the suspicious activity
def log_suspicious_activity(username, reason):
    logging.info(f"Suspicious activity detected: User: {username}, Reason: {reason}")

@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the input contains suspicious patterns
        if is_suspicious_input(username) or is_suspicious_input(password):
            log_suspicious_activity(username, "Potential SQL Injection attempt in login")
            return "Suspicious input detected. Login attempt blocked."
        
        # Whitelisting input
        if not is_valid_input(username) or not is_valid_input(password):
            return "Invalid input. Only alphanumeric characters are allowed."
        
        connection = sqlite3.connect('demo.db')
        cursor = connection.cursor()
        
        # Using a parameterized query to prevent SQL injection
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        
        user = cursor.fetchone()
        connection.close()

        if user:
            message = "Login successful!"
            return redirect(url_for('search'))
        else:
            message = "Login failed!"
            # Log failed login attempts
            logging.info(f"Failed login attempt for username: {username}")

    return render_template_string(open('login.html').read(), message=message)

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
    app.run(debug=True, port=5001)
