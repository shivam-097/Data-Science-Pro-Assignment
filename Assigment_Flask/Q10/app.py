from flask import Flask, render_template

app = Flask(__name__)

# Route for handling 404 errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Route for handling 500 errors
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Custom error page for other errors
@app.errorhandler(Exception)
def other_error(error):
    return render_template('error.html', error=error), 500

@app.route('/demo_error')
def demo_error():
    return render_template('500.html'), 500

# Main route
@app.route('/')
def index():
    return 'Hello, Flask!'

if __name__ == '__main__':
    app.run(debug=True)
