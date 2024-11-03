""" 
Accessing the Vulnerable and Secure Endpoints:

Vulnerable: http://127.0.0.1:5000/system_info?command=whoami (allows arbitrary commands, e.g., whoami; dir).
Secure: http://127.0.0.1:5000/system_info_secure (only allows commands in the dropdown list, based on the detected platform).
 """


from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import re
import logging
import subprocess
import platform

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
def log_suspicious_activity(details):
    logging.info(f"Suspicious activity detected: {details}")

# Detect operating system to run compatible commands
def get_valid_commands():
    if platform.system() == "Windows":
        # Windows-compatible commands
        return {
            'whoami': ['whoami'],
            'date': ['echo', '%date%'],
            'uptime': ['net', 'statistics', 'workstation']  # Windows command for uptime
        }
    else:
        # Unix-compatible commands
        return {
            'whoami': ['whoami'],
            'date': ['date'],
            'uptime': ['uptime']
        }

@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the input contains suspicious patterns
        if is_suspicious_input(username) or is_suspicious_input(password):
            log_suspicious_activity(f"Potential SQL Injection attempt in login for user: {username}")
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
            return redirect(url_for('system_info'))
        else:
            message = "Login failed!"
            # Log failed login attempts
            logging.info(f"Failed login attempt for username: {username}")

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

# Vulnerable system info route (for demonstration purposes)
@app.route('/system_info', methods=['GET'])
def system_info():
    # Get the command parameter from the user (vulnerable to command injection)
    command = request.args.get('command', 'whoami')  # Default to 'whoami'
    
    # Vulnerable: Directly passing user input to the shell command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Render the command output
    return render_template_string("""
        <h2>System Info</h2>
        <pre>{{ content }}</pre>
        <p>Try entering different commands to test the vulnerability.</p>
        <form method="get" action="/system_info">
            Command: <input type="text" name="command">
            <input type="submit" value="Execute">
        </form>
    """, content=result.stdout)

# Secure version of system_info route with allowlist and logging
@app.route('/system_info_secure', methods=['GET'])
def system_info_secure():
    VALID_COMMANDS = get_valid_commands()
    command_key = request.args.get('command', 'whoami')
    command = VALID_COMMANDS.get(command_key)

    # If an invalid command is detected, log it and return an error
    if not command:
        log_suspicious_activity(f"Invalid command attempt: {command_key}")
        return "Invalid command.", 400

    # Securely run the command without shell=True
    result = subprocess.run(command, capture_output=True, text=True)
    return render_template_string("""
        <h2>Secure System Info</h2>
        <pre>{{ content }}</pre>
        <p>Select a command to execute securely:</p>
        <form method="get" action="/system_info_secure">
            <select name="command">
                <option value="whoami">whoami</option>
                <option value="date">date</option>
                <option value="uptime">uptime</option>
            </select>
            <input type="submit" value="Execute">
        </form>
    """, content=result.stdout)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
