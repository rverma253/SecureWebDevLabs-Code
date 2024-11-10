from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired, EqualTo
from werkzeug.security import check_password_hash

app = Flask(__name__)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# In-memory storage for users (in place of a database)
users = {}

# User model extending UserMixin for Flask-Login compatibility
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=8),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])

# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# Load user from users dictionary for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username in users:
            flash("Username already taken!")
            return redirect(url_for('register'))

        # Hash the password before storing it
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(id=username, username=username, password=hashed_password)
        users[username] = user
        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = users.get(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully!")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.")
    
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Hello, {current_user.username}! Welcome to your dashboard."

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
