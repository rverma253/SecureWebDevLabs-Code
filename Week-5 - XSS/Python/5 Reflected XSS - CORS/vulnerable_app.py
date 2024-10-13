from flask import Flask, request, render_template, make_response, session
app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/search')
def search():
    query = request.args.get('query', '')
    session['username'] = 'JohnDoe'  # Setting a session cookie
    response = make_response(render_template('search.html', query=query))
    return response

if __name__ == "__main__":
    app.run(port=5000, debug=True)
