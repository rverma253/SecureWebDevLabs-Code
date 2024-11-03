from flask import Flask, request, render_template_string
import sqlite3
import subprocess
import os

app = Flask(__name__)

# Initialize the database with sample user data
def init_db():
    with sqlite3.connect('demo.db') as db:
        db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)')
        db.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'password123')")
        db.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('bob', 'bobpass')")
        db.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('alice', 'alicepass')")

# Create a default log file with some content
def create_default_log():
    if not os.path.exists('default.log'):
        with open('default.log', 'w') as f:
            f.write("Sample log file content.\n")
            f.write("Log entry 1: User logged in.\n")
            f.write("Log entry 2: User attempted to view logs.\n")

# Login route to authenticate users
@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = sqlite3.connect('demo.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password))
        user = cursor.fetchone()
        connection.close()

        if user:
            message = "Login successful!"
        else:
            message = "Login failed!"

    # Basic HTML for login form
    return render_template_string("""
        <html>
        <head><title>Login</title></head>
        <body>
            <h2>Login</h2>
            <form method="POST" action="/login">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Login">
            </form>
            <p>{{ message }}</p>
        </body>
        </html>
    """, message=message)

# Vulnerable route to display contents of a file specified by the user
@app.route('/view_logs', methods=['GET'])
def view_logs():
    filename = request.args.get('filename', 'default.log')  # Default file is 'default.log'
    
    # Vulnerable to command injection as it uses shell=True with user input
    command = f"cat {filename}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Render the output of the command to the page
    return render_template_string("""
        <html>
        <head><title>View Logs</title></head>
        <body>
            <h2>Log Contents</h2>
            <pre>{{ content }}</pre>
        </body>
        </html>
    """, content=result.stdout)

if __name__ == "__main__":
    init_db()
    create_default_log()
    app.run(debug=True, port=5000)
