from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock user database with attributes
users = {
    'admin': {'password': 'admin123', 'role': 'admin', 'location': 'office'},
    'remote_user': {'password': 'remote123', 'role': 'user', 'location': 'remote'}
}

# ABAC policy
def abac_policy(user, resource):
    if user['role'] == 'admin':
        return True
    if user['role'] == 'user' and user['location'] == 'office' and resource == 'resource':
        return True
    return False

@app.route('/')
def home():
    return render_template('home_abac.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    resource = request.form['resource']

    if username in users and users[username]['password'] == password:
        if abac_policy(users[username], resource):
            return redirect(url_for('resource'))
    return redirect(url_for('home'))

@app.route('/resource')
def resource():
    return 'Access to Resource Granted'

if __name__ == '__main__':
    app.run(debug=True)
