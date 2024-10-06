from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)

# Route for rendering the login form
@app.route('/')
def index():
    return render_template('form.html')

# Route for handling login logic and setting a secure cookie
@app.route('/login', methods=['POST'])
def login():
    # Get the form data
    username = request.form['username']
    password = request.form['password']

    # Example logic to check username and password
    if username == "admin" and password == "password":
        # Create a response and set a secure cookie
        resp = make_response(redirect(url_for('welcome')))
        resp.set_cookie('secureCookie', username, secure=True, httponly=True, samesite='Strict', max_age=60*60*24) # Security Parameter for Cookie
        #resp.set_cookie('secureCookie', username, max_age=60*60*24)
        return resp
    else:
        return "Login failed. Please try again."

# Route to retrieve and display the secure cookie
@app.route('/welcome')
def welcome():
    secure_cookie = request.cookies.get('secureCookie')
    if secure_cookie:
        return f"Welcome back, {secure_cookie}! Your login was successful."
    else:
        return 'No secure cookie set. Please log in first.'

# Route to clear the cookie
@app.route('/logout')
def logout():
    resp = make_response("You've been logged out.")
    resp.set_cookie('secureCookie', '', expires=0)  # Remove the cookie
    return resp

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')  # Ad-hoc SSL for secure connection # Warning will be there, as it is self signed certificate.
    #app.run(debug=True)
