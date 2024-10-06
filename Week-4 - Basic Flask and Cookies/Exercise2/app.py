from flask import Flask, render_template

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def hello_world():
    return render_template('index.html')  # Rendering the HTML file

if __name__ == '__main__':
    app.run(debug=True)
