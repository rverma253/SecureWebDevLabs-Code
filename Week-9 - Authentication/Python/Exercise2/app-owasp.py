#pip install Flask-WTF WTForms

from flask import Flask, request, render_template_string, redirect, url_for, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YourSecretKey'  # Replace with a real secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

def password_complexity_check(form, field):
    password = field.data
    if not any(char.islower() for char in password):
        raise ValidationError('Password must include at least one lowercase letter.')
    if not any(char.isupper() for char in password):
        raise ValidationError('Password must include at least one uppercase letter.')
    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must include at least one number.')
    if not any(char in set('!@#$%^&*()') for char in password):
        raise ValidationError('Password must include at least one special character (!@#$%^&*()).')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', [validators.Length(min=1, max=50)])
    last_name = StringField('Last Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=8, message='Password should be at least 8 characters long'),
        password_complexity_check
    ])
    confirm = PasswordField('Repeat Password')

@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        password = form.password.data

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(first_name=first_name, last_name=last_name, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('register_success'))
    return render_template('registration_form2.html', form=form)

@app.route('/success')
def register_success():
    return 'Registration successful!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
