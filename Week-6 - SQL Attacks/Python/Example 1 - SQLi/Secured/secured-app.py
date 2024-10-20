from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('demo.db') as db:
        db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
        db.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', 'password123'))
        db.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('bob', 'bobpass'))
        db.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('alice', 'alicepass'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = sqlite3.connect('demo.db')
        cursor = connection.cursor()
        
        # Using a parameterized query to prevent SQL injection
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        
        user = cursor.fetchone()
        connection.close()

        if user:
            message = "Login successful!"
        else:
            message = "Login failed!"

    return render_template_string(open('login.html').read(), message=message)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
