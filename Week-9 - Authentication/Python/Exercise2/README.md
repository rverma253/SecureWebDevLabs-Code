# Registration - OWASP Guideline

This project is a simple Flask web application that demonstrates secure user registration by following best practices from the OWASP (Open Web Application Security Project) guidelines. It includes password complexity requirements and secure password hashing to protect user information.

## Features

- **User Registration**: Allows users to register with first name, last name, username, and a password that meets specific security criteria.
- **Password Complexity Requirements**: Enforces password strength by requiring at least:
  - One lowercase letter
  - One uppercase letter
  - One digit
  - One special character (`!@#$%^&*()`)
- **Secure Password Storage**: Passwords are hashed using `bcrypt` for strong encryption, ensuring passwords are not stored in plain text.

## Technologies Used

- **Flask**: Micro web framework used for building the web application.
- **SQLite**: Lightweight database used to store user information.
- **Flask-WTF** and **WTForms**: For form validation, including custom password complexity checks.
- **Flask-Bcrypt**: For secure password hashing.

## Setup Instructions

1. **Install the required packages**:
   ```bash
   pip install Flask Flask-Bcrypt Flask-SQLAlchemy Flask-WTF WTForms
