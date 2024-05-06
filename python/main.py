from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

@app.before_request
def log_request():
    # Get the current time in a readable format
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Logs the method, the URL, User-Agent, and the timestamp of the request
    app.logger.info(f"{current_time} - Request: {request.method} {request.url} - User-Agent: {request.headers.get('User-Agent')}")

@app.route('/')
def home():
    return jsonify(message="Welcome to the Home page!")

@app.route('/about')
def about():
    return jsonify(message="This is the about page.")

@app.route('/api/data')
def api_data():
    return jsonify(data=[{"id": 1, "value": "Item 1"}, {"id": 2, "value": "Item 2"}])

@app.route('/ui', methods=['GET', 'POST'])
def user_interface():
    if request.method == 'POST':
        category = request.form['category']
        # Do the request to Elasticsearch
        #
        #
        number = 12 # assign result of Elasticsearch query to this variable
        return render_template('ui.html', number=number, category=category)
    return render_template('ui.html', number=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)