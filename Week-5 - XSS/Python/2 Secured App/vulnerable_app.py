from flask import Flask, request, render_template, redirect, url_for, make_response

app = Flask(__name__)

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hardcoded credentials
        if username == 'admin' and password == 'pass':
            # Set a cookie to track the user (vulnerable to XSS)
            resp = make_response(redirect(url_for('post_message')))
            resp.set_cookie('user', username, max_age=60*60*24)  # Cookie is set without HttpOnly or Secure flags
            return resp
        else:
            return "Login failed. Try again."

    return render_template('login.html')

# Route to post a message (only accessible after login)
@app.route('/post', methods=['GET', 'POST'])
def post_message():
    user = request.cookies.get('user')
    if not user:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    if request.method == 'POST':
        message = request.form.get('message', '')
        # Reflecting the message directly (vulnerable to XSS)
        return render_template('post.html', user=user, message=message)

    return render_template('post.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
