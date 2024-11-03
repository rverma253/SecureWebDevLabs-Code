from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Add a response decorator to include anti-clickjacking headers
@app.after_request
def add_security_headers(response):
    # Prevents the app from being embedded in an iframe
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "frame-ancestors 'none';"
    return response

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == "admin" and password == "password":
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials. Please try again.")
    return render_template('login.html')

# Route for dashboard page
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Route to log out
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
