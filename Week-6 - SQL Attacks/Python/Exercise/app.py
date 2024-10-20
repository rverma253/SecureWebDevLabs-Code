from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Placeholder: Function to initialize the database
def init_db():
    """
    Students should implement this function to create the database tables,
    such as a `users` table with columns for id, username, email, and password.
    """
    pass

# Placeholder: Function to validate user input
def is_valid_input(input_data):
    """
    Students should implement input validation logic here (whitelisting).
    Example: Ensure the username is alphanumeric, the email is in a valid format, etc.
    """
    pass

# Placeholder: Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Students should capture the input data here
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Placeholder: Validate the input using the is_valid_input function
        # Students should call their validation functions here and handle any errors
        
        # TODO: Implement input validation and whitelisting
        # Example: Ensure username is alphanumeric and email is valid

        # Placeholder: Use parameterized queries to insert the new user into the database
        # Example: conn = sqlite3.connect('demo.db')
        #          cursor = conn.cursor()
        #          cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        #          conn.commit()
        #          conn.close()

        # Placeholder: Handle registration success or errors and redirect to login
        return redirect(url_for('login'))

    # Render the registration template
    return render_template('register.html')

# Placeholder: Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Students should capture the input data here
        username = request.form['username']
        password = request.form['password']

        # Placeholder: Validate the input using the is_valid_input function
        # Students should call their validation functions here and handle any errors

        # Placeholder: Use parameterized queries to check if the user exists in the database
        # Example: conn = sqlite3.connect('demo.db')
        #          cursor = conn.cursor()
        #          cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        #          user = cursor.fetchone()

        # Placeholder: Handle login success or failure
        if user:
            return redirect(url_for('profile', username=username))
        else:
            return "Login failed! Please try again."

    # Render the login template
    return render_template('login.html')

# Placeholder: Profile route (view/edit user profile)
@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    # Placeholder: Fetch the user's current profile details from the database
    # Example: conn = sqlite3.connect('demo.db')
    #          cursor = conn.cursor()
    #          cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    #          user = cursor.fetchone()

    if request.method == 'POST':
        # Students should capture the input data for updating the profile
        new_email = request.form['email']
        new_password = request.form['password']

        # Placeholder: Validate the new input using the is_valid_input function
        # Placeholder: Use parameterized queries to update the user's profile in the database

        # Handle profile update success
        return "Profile updated successfully!"

    # Render the profile template with the user's data
    return render_template('profile.html', user=user)

# Placeholder: Search route
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Students should capture the search query input
        search_query = request.form['search_query']

        # Placeholder: Validate the search input using the is_valid_input function
        # Placeholder: Use parameterized queries to search the database in read-only mode
        # Example: conn = sqlite3.connect('file:demo.db?mode=ro', uri=True)
        #          cursor = conn.cursor()
        #          cursor.execute("SELECT username, email FROM users WHERE username LIKE ? OR email LIKE ?", (f'%{search_query}%', f'%{search_query}%'))
        #          results = cursor.fetchall()

        # Render the search results page with the search results
        return render_template('search_results.html', results=results)

    # Render the search template
    return render_template('search.html')

if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(debug=True, port=5001)
