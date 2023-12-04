from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/<cityname>')
def homepage(cityname):
    return render_template('index.html', city = cityname)

if __name__== '__main__':
    app.run(host='0.0.0.0', port=8001)
