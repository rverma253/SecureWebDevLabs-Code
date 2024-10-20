from flask import Flask, request, render_template_string
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['demoDB']
users = db['users']

def init_db():
    users.insert_one({'username': 'admin', 'password': 'password123'})
    users.insert_one({'username': 'bob', 'password': 'bobpass'})
    users.insert_one({'username': 'alice', 'password': 'alicepass'})

@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.find_one({'username': username, 'password': password})

        if user:
            message = "Login successful!"
        else:
            message = "Login failed!"

    return render_template_string(open('login.html').read(), message=message)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
