import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET KEY'] = 'hbr14asb20hak0moc4636'
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * from posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']


        if not title:
            flash('Title is required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, price) VALUES (?, ?)',
                         (title, price))
            conn.commit()
            conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post= get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        image = request.form['image']

        if not title:
            flash('Title is required')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, price = ?, image = ?'
                         'WHERE id = ?', (id, title, price, image))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
    post=get_post(id)
    conn=get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    flash('"{}" was deleted'.format(post['title']))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
