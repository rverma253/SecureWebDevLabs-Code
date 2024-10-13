from flask import Flask, request, render_template, redirect, url_for, make_response, session
from markupsafe import escape

app = Flask(__)
app.secret_key = 'supersecretkey'  # Needed for session management

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hardcoded credentials
        if username == 'admin' and password == 'pass':
            # Set a secure session
            session['user'] = username
            return redirect(url_for('post_message'))
        else:
            return "Login failed. Try again."

    return render_template('login.html')

# Route to post a message (only accessible after login)
@app.route('/post', methods=['GET', 'POST'])
def post_message():
    user =session.get('user')
    if not user:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    if request.method == 'POST':
        message = request.form.get('message', '')
        # Sanitize the message input
        message = escape(message)
        return render_template('post.html', user=escape(user), message=message)

    return render_template('post.html', user=escape(user))

# Applying Content Security Policy (CSP)
@app.after_request
def apply_csp(response):
    response.headers['Content-Security-Policy'] = "default-src 'self';"
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
