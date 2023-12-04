from flask import Flask, render_template, request, session
app = Flask(__name__)

app.secret_key = 'BAD_SECRET_KEY'


@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('index.html',name = session.get('name'))

# Create a route of Submit
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    session['name'] = name
    return render_template('index.html',name=name)

if __name__ == '__main__':
    app.run()