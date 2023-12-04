from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route('/batch')
def batch():
    return render_template('batch.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)