from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock user database with attributes
users = {
    'admin': {'password': 'admin123', 'time': 'day'},
    'night_shift': {'password': 'night123', 'time': 'night'}
}

# Access rules based on time
access_rules = {
    'day': ['admin'],
    'night': ['night_shift']
}

@app.route('/')
def home():
    return render_template('home_rac.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    time = request.form['time']

    if username in users and users[username]['password'] == password and time in access_rules[users[username]['time']]:
        return redirect(url_for('dashboard'))
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    return 'Access Granted'

if __name__ == '__main__':
    app.run(debug=True)
