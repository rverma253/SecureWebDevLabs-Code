from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock user database with clearance levels
users = {
    'admin': {'password': 'admin123', 'clearance': 'top_secret'},
    'user': {'password': 'user123', 'clearance': 'secret'},
    'guest': {'password': 'guest123', 'clearance': 'confidential'}
}

# Resource classification
resources = {
    'top_secret': ['admin'],
    'secret': ['admin', 'user'],
    'confidential': ['admin', 'user', 'guest']
}

@app.route('/')
def home():
    return render_template('home_mac.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]['password'] == password:
        clearance = users[username]['clearance']
        return redirect(url_for(resources[clearance][0]))
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    return render_template('admin_mac.html')

@app.route('/user')
def user():
    return render_template('user_mac.html')

@app.route('/guest')
def guest():
    return render_template('guest_mac.html')

if __name__ == '__main__':
    app.run(debug=True)
