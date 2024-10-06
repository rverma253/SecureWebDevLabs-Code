# Secure Web Development - Week-4 Exercises

This repository contains four exercises designed to help students learn the basics of web development using Flask for the course "Secure Web Development." Each exercise introduces new concepts in Flask, progressing from simple web apps to ones with forms, CSS, and cookies.

## Prerequisites

Before running the exercises, make sure you have the following installed on your system:
- Python 3.x: [Download Python](https://www.python.org/downloads/)
- Flask: You can install Flask using `pip` by running the following command:
  ```bash
  pip install flask
  ```

## How to Run the Exercises

1. Clone this repository to your local machine.
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Navigate to the folder of the exercise you want to run (e.g., `Exercise 1`, `Exercise 2`, etc.).

3. Start the Flask application by running the following command inside each exercise folder:
    ```bash
    python app.py
    ```
   or for Exercise 1, use:
   ```bash
   python appold.py
   ```

4. Open a browser and navigate to `http://127.0.0.1:5000/` to view the app.

---

## Exercise 1: Simple Flask App

- **File**: `appold.py`
- **Description**: A single-page Flask app with a welcome message. The page is served at the root URL (`/`).
- **Goal**: To introduce students to the basics of Flask, such as creating routes and rendering responses from a Python file.

### Key Concepts:
- Basic Flask structure
- Flask routes
- Serving static content

---

## Exercise 2: Flask App with Template

- **Files**: `app.py`, `templates/index.html`
- **Description**: A Flask app that separates HTML from Python logic by placing the HTML content inside a template file (`index.html`).
- **Goal**: To understand Flask’s template system and how it integrates with Python code to render HTML files dynamically.

### Key Concepts:
- Flask templates (`Jinja2`)
- Rendering HTML from a template file

---

## Exercise 3: Flask App with Form and CSS

- **Files**: `app.py`, `templates/form.html`, `static/style.css`
- **Description**: A simple login page using Flask. This app includes one HTML form (`form.html`) for logging in, and a CSS file (`style.css`) for basic styling. The login credentials are "admin" and "password".
- **Goal**: To demonstrate how to handle form data in Flask and apply CSS for styling.

### Key Concepts:
- Handling POST requests
- Flask form handling (`request.form`)
- Serving static files (CSS)

---

## Exercise 4: Flask App with Cookies

- **Files**: `app.py`, `templates/form.html`, `static/style.css`
- **Description**: This exercise builds on Exercise 3 by adding secure cookie handling to the login page. The app sets and retrieves cookies when a user logs in successfully.
- **Goal**: To introduce the concept of secure cookies in Flask.

### Key Concepts:
- Flask cookies (`request.cookies`, `set_cookie`)
- Secure cookies (`httponly`, `secure`, `samesite` attributes)
- You may some warning in browser - it is because of selfsigned certificated. Look at https://letsencrypt.org/getting-started/

---

## Running the Applications

Each exercise can be run individually by navigating to its respective folder and executing the Python script (`app.py` or `appold.py`).

For example, to run Exercise 1:
```bash
cd Exercise1
python appold.py
```

To run Exercise 2:
```bash
cd Exercise2
python app.py
```

After starting the Flask development server, you can open your browser and access the app at:
```
http://127.0.0.1:5000/
```

---

## Additional Resources

- **Flask Documentation**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **Python Documentation**: [https://docs.python.org/3/](https://docs.python.org/3/)
- **Flask Quickstart**: [https://flask.palletsprojects.com/en/2.0.x/quickstart/](https://flask.palletsprojects.com/en/2.0.x/quickstart/)

---

These exercises are designed to progressively build your understanding of secure web development using Flask. Feel free to explore the code and modify it to deepen your learning.
