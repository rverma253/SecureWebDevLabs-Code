from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock user database
users = {
    'admin': {'password': 'admin123', 'access': ['home', 'admin', 'user']},
    'user': {'password': 'user123', 'access': ['home', 'user']}
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]['password'] == password:
        return redirect(url_for(users[username]['access'][0]))
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/user')
def user():
    return render_template('user.html')

if __name__ == '__main__':
    app.run(debug=True)
