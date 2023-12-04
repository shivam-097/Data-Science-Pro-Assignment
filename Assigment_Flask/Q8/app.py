from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Configuration for Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Example User class for demonstration (Replace this with a proper User model)
class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

# In-memory list for user storage (replace this with a database)
users = [
    User(1, 'user1'),
    User(2, 'user2')
]

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((user for user in users if user.username == username), None)

        if user and password == 'password':  # Insecure password check, replace this with proper authentication
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']

        if next((user for user in users if user.username == username), None) is None:
            new_user = User(len(users) + 1, username)
            users.append(new_user)
            login_user(new_user)
            flash('Registration and login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username already taken. Choose a different one.', 'error')

    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
