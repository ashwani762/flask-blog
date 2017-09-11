from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from data import Articles
import sqlite3 as sql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

DATABASE = 'E:\\PyCharm\\Proj\\blog\\blog.db'

Articles = Articles()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)


@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)


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
    app.secret_key='secretcantbehold'
    app.run(debug=True, port=80)
