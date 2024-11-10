# pip install Flask-SQLAlchemy


from flask import Flask, request, render_template_string
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(first_name=first_name, last_name=last_name, username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return 'Registration successful!'
        else:
            return 'Passwords do not match.'

    return render_template_string(open('registration_form.html').read())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch the user by username
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return 'Login successful!'
        else:
            return 'Invalid username or password.'

    return render_template_string(open('login.html').read())


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    #db.create_all()
    app.run(debug=True)
