from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
from pathlib import Path

app = Flask(__name__)

DATABASE = 'database.db'

app.config['DATABASE'] = DATABASE
app.config['SECRET_KEY'] = 'your_secret_key'


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def create_table():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    if 'db' not in g:
        g.db = connect_db()
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT id, name FROM items')
    items = cur.fetchall()
    return render_template('index.html', items=items)


@app.route('/add', methods=['POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']

        db = get_db()
        db.execute('INSERT INTO items (name) VALUES (?)', [name])
        db.commit()

    return redirect(url_for('index'))


@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    db = get_db()

    if request.method == 'POST':
        new_name = request.form['new_name']
        db.execute('UPDATE items SET name = ? WHERE id = ?', [new_name, item_id])
        db.commit()
        return redirect(url_for('index'))

    cur = db.execute('SELECT id, name FROM items WHERE id = ?', [item_id])
    item = cur.fetchone()

    return render_template('edit.html', item=item)


@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    db = get_db()
    db.execute('DELETE FROM items WHERE id = ?', [item_id])
    db.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Create the database and table if they don't exist
    database_path = Path(app.config['DATABASE'])
    if not database_path.is_file():
        create_table()

    app.run(debug=True)
