# Flask Security Framework
A basic Python Flask web application implementing a simple authentication system with registration, login, and dashboard access. This application demonstrates secure password hashing, session management, and form validation using Flask's extensions.

## Features
- User Registration: Allows new users to register with a username and password.
- Login: Authenticates users based on their registered credentials.
- Dashboard: Protected route accessible only to authenticated users.
- Logout: Allows users to end their session.
- Password Security: Utilizes bcrypt for password hashing.
- Session Management: Implements session-based authentication with Flask-Login.

## Technologies Used
- Flask: Lightweight web application framework.
- Flask-Login: Manages user session and authentication.
- Flask-Bcrypt: Provides secure password hashing.
- Flask-WTF: Adds form handling and validation.
- WTForms: Validates form inputs.
- Werkzeug Security: Verifies password hash during login.

## References
- Flask-Login - https://flask-login.readthedocs.io/en/latest/
- Flask-Bcrypt - https://flask-bcrypt.readthedocs.io/en/1.0.1/
- Video Tutorial - https://www.youtube.com/watch?v=71EU8gnZqZQ
- https://github.com/arpanneupane19/Python-Flask-Authentication-Tutorial