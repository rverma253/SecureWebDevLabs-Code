from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Used for session management

# Enabling CSRF protection
csrf = CSRFProtect(app)

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check for valid credentials
        if username == 'admin' and password == 'pass':
            session['user'] = username
            return redirect(url_for('transfer_funds'))
        else:
            return "Login failed. Try again."

    return render_template('login.html')

# Route to allow transferring funds (now protected from CSRF)
@app.route('/transfer', methods=['GET', 'POST'])
def transfer_funds():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        amount = request.form['amount']
        # Process the fund transfer
        return f"Transferred {amount} successfully!"

    return render_template('securetransfer.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
