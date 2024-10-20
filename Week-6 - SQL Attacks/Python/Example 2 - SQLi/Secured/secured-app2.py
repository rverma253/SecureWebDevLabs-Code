'''
Key Changes

    Whitelisting Input:
        Added the is_valid_input function, which checks if the input contains only alphanumeric characters using a regular expression (^[a-zA-Z0-9]+$).
        This function is applied both in the login and search routes to validate the inputs for username, password, and search queries.
        If the input contains any non-alphanumeric characters, the app rejects it with an error message.

    Simulated Read-Only Permissions:
        For the search operation, the database is opened in read-only mode using sqlite3.connect('file:demo.db?mode=ro', uri=True).
        This ensures that even if an attacker attempts an SQL injection, the query can only read data, not modify it.

    Security Improvements:
        Combined parameterized queries with input whitelisting and read-only database access to create multiple layers of defense against SQL injection attacks.
'''

from flask import Flask, request, render_template_string, render_template, redirect, url_for
import sqlite3
import re  # Regular expressions for whitelisting

app = Flask(__name__)

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

@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
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

    return render_template_string(open('login.html').read(), message=message)

# Route for the search page (Secured with Parameterized Queries and Read-Only Permissions)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']

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
