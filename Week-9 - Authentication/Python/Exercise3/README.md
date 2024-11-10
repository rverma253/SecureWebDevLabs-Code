# Registration with Password Strength Validation

This is a Flask-based registration application that incorporates secure password hashing and a password strength meter. The password strength meter visually indicates the strength of the password and estimates the time it would take to crack it, following secure password practices and leveraging the zxcvbn library for password analysis.

## Features

- **User Registration**: Allows users to register with details such as first name, last name, username, and password.
- **Password Complexity Requirements**: Enforces password strength by requiring:
  - At least one lowercase letter
  - At least one uppercase letter
  - At least one digit
  - At least one special character (`!@#$%^&*()`)
  - Minimum of 8 characters
- **Password Strength Meter**: Displays the strength of the password and an estimated time to crack it, using the zxcvbn library.
- **Secure Password Storage**: Passwords are hashed with `bcrypt` for secure storage.

## Technologies Used

- **Flask**: Web framework for building the application.
- **SQLite**: Database for storing user information.
- **Flask-WTF and WTForms**: For form handling and validation.
- **Flask-Bcrypt**: For secure password hashing.
- **zxcvbn**: JavaScript library to estimate password strength. CHeck the HTML page for the JS link.

## Setup Instructions

1. **Install the required packages**:
   ```bash
   pip install Flask Flask-Bcrypt Flask-SQLAlchemy Flask-WTF WTForms
