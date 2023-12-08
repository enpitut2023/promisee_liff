# main.py
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    return render_template('index.html', api_key=api_key)

if __name__ == '__main__':
    app.run(debug=True)
