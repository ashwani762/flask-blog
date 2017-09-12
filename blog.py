from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
# from data import Articles
import sqlite3 as sql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

DATABASE = 'E:\\PyCharm\\Proj\\blog\\blog.db'

# Articles = Articles()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    # cursor
    try:
        db = sql.connect(DATABASE)
        cur = db.cursor()
        cur.execute('SELECT * from articles')
        articles = cur.fetchall()

        if len(articles) > 0:
            return render_template('articles.html', articles=articles)
        else:
            msg = 'No articles Found'
            return render_template('articles.html', msg=msg)
    except:
        print("Error reading database")
    finally:
        db.close()

@app.route('/article/<string:id>/')
def article(id):
    # cursor
    try:
        db = sql.connect(DATABASE)
        cur = db.cursor()
        cur.execute('SELECT * from articles where id = ?',id)
        article = cur.fetchone()

    except:
        print("Error reading database")
    finally:
        db.close()
    return render_template('article.html', article=article)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # cursor
        try:
            db = sql.connect(DATABASE)
            cur = db.cursor()
            cur.execute('INSERT INTO users(name, email, username, password) VALUES (?,?,?,?)',
                        (name, email, username, password))

            # commit

            db.commit()
        except:
            print("Error")
        finally:
            db.close()

        flash('Registeration done', 'success')
        return redirect('/')
    return render_template('register.html', form=form)


# login

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        # Cursor

        try:
            db = sql.connect(DATABASE)
            cur = db.cursor()
            # get user
            result = cur.execute("SELECT * FROM users WHERE username = ?", [username])
            data = cur.fetchall()
            # print(result)

            if len(data) != 0:
                # get stored hash
                # get first row password field
                password = data[0][4]

                if sha256_crypt.verify(password_candidate, password):
                    # Passed
                    session['logged_in'] = True
                    session['username'] = username

                    flash('You are now logged in', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    error = 'Invalid Login'
                    return render_template('login.html', error=error)
            else:
                error = 'Username not found'
                return render_template('login.html', error=error)
        except:
            print('Error connecting to databse')
        finally:
            db.close()
    return render_template('login.html')


# check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized acess', 'danger')
            return redirect(url_for('login'))

    return wrap


# logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    # cursor
    try:
        db = sql.connect(DATABASE)
        cur = db.cursor()
        cur.execute('SELECT * from articles')
        articles = cur.fetchall()

        if len(articles) > 0:
            return render_template('dashboard.html', articles = articles)
        else:
            msg = 'No articles Found'
            return render_template('dashboard.html', msg=msg)
    except:
        print("Error reading database")
    finally:
        db.close()


# Article class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])


@app.route('/add_article', methods=['POST', 'GET'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # create cursor
        # cursor
        try:
            db = sql.connect(DATABASE)
            cur = db.cursor()
            cur.execute('INSERT INTO articles(title, body, author) VALUES (?,?,?);',
                        (title, body, session['username']))
            # commit
            db.commit()
            flash('Article created', 'success')
        except:
            print("Error inserting article")
        finally:
            db.close()
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)


# @app.route('/users/<int:id>')
# def users(id):
#     names = []
#     # cursor
#     try:
#         db = sql.connect(DATABASE)
#         cur = db.cursor()
#         cur.execute('select name from users;')
#         names = cur.fetchall()
#
#         # commit
#
#         db.commit()
#     except:
#         print("Error")
#     finally:
#         db.close()
#
#     return render_template('users.html',names=names)

if __name__ == '__main__':
    app.secret_key = 'secretcantbehold'
    app.run(debug=True, port=80)
