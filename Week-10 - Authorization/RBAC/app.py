from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock user database with roles
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'manager': {'password': 'manager123', 'role': 'manager'},
    'employee': {'password': 'employee123', 'role': 'employee'}
}

@app.route('/')
def home():
    return render_template('home_rbac.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]['password'] == password:
        role = users[username]['role']
        return redirect(url_for(role))
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    return render_template('admin_rbac.html')

@app.route('/manager')
def manager():
    return render_template('manager_rbac.html')

@app.route('/employee')
def employee():
    return render_template('employee_rbac.html')

if __name__ == '__main__':
    app.run(debug=True)
