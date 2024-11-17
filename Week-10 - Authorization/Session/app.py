from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key

@app.route('/')
def home():
    # Display the session ID if a user is logged in
    if 'username' in session:
        session_id = request.cookies.get('session')
        return f'Welcome {session["username"]}! Your session ID is {session_id}. <br><a href="/logout">Logout</a>'
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']  # Verify password in a real app
    session['username'] = username
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
