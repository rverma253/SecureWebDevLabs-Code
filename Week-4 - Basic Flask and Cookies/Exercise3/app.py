from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/login', methods=['POST'])
def login():
    # Get the form data
    username = request.form['username']
    password = request.form['password']

    # You can add logic to check username and password here
    if username == "admin" and password == "password":  # Example condition
        return f"Welcome, {username}!"
    else:
        return "Login failed. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
