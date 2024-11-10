# Flask Authentication App

This is a simple Flask web application that demonstrates basic user authentication, including user registration and login. The project uses SQLite for the database and Flask-Bcrypt for password hashing to enhance security.

## Features

- **User Registration**: Users can register by providing their first name, last name, username, and password.
- **Login**: Users can log in using their registered username and password. The password is verified using hashing for added security.

## Technologies Used

- **Flask**: Micro web framework used for building the web application.
- **SQLite**: Lightweight database used to store user information.
- **Flask-Bcrypt**: For secure password hashing.

## Setup Instructions

1. **Install the required packages**:
   ```bash
   pip install Flask Flask-Bcrypt Flask-SQLAlchemy
