from flask import Flask, request, render_template
import sqlite3
from jinja2 import escape

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comment TEXT
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    create_table()
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        comment = request.form.get('comment')
        
        user_comment = request.args.get('comment')
        safe_comment = escape(user_comment)
        
        cursor.execute('INSERT INTO comments (comment) VALUES (?)', (safe_comment,))
        conn.commit()

    cursor.execute('SELECT * FROM comments')
    comments = cursor.fetchall()
    conn.close()

    return render_template('index.html', comments=comments)

if __name__ == "__main__":
    app.run(ssl_context='adhoc')