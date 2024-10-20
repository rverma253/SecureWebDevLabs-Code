from flask import Flask, request, render_template_string, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('demo.db') as db:
        db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)')
        db.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'password123')")
        db.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('bob', 'bobpass')")
        db.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('alice', 'alicepass')")

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
            return redirect(url_for('search'))
        else:
            message = "Login failed!"

    return render_template_string(open('login.html').read(), message=message)

# Route for the search page (Secured with Parameterized Queries)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']

        # Secure query (Using parameterized queries to prevent SQL injection)
        conn = sqlite3.connect('demo.db')
        cursor = conn.cursor()
        query = "SELECT username FROM users WHERE username LIKE ?"
        cursor.execute(query, ('%' + search_query + '%',))
        results = cursor.fetchall()
        conn.close()

        return render_template('search_results.html', results=results)

    return render_template('search.html')


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)
