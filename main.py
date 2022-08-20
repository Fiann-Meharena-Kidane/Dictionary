from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from tools import *
from models import *


from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

import json
import requests
import os

# api credentials
app_id = os.environ.get('dictionary_api_id')
app_key = os.environ.get('dictionary_api_key')
endpoint = "entries"

language_code = "en-us"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='secret'
my_db = SQLAlchemy(app)


login_manager=LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
def choose():
    # user either logs in or sign up,
    return render_template('index.html', current_user=False)


@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    word = request.form.get('word')
    # gets word and pass it to request handler function,
    response = request_handler(endpoint=endpoint,
                               app_key=app_key,
                               app_id=app_id,
                               language_code=language_code,
                               word=word)
    # each word user searched for is saved for a moment,
    new_word_entry = Words(
        word=word,
    )

    my_db.session.add(new_word_entry)
    my_db.session.commit()

    saved_words=Saved.query.all()
    list_of_saved_words=[]
    for row in saved_words:
        list_of_saved_words.append(row.word)

    if word in list_of_saved_words:
        # if word already exists in favo, don't display the add button,
        return render_template('index.html',
                               definitions=shorten_list(response['list_of_definitions']),
                               examples=shorten_list(response['list_of_examples']),
                               word_found=True,
                               message='Ah! Got it!',
                               save='saved')
    else:
        return render_template('index.html',
                               definitions=shorten_list(response['list_of_definitions']),
                               examples=shorten_list(response['list_of_examples']),
                               word_found=True,
                               message='Ah! Got it!',
                               )


@app.route('/save', methods=['POST','GET'])
def save():
    list_of_rows=Words.query.all()
    try:
        last_row=list_of_rows[-1]
    except IndexError:
        return 'index error'
    else:
        pass

    new_word=Saved(
        word=last_row.word
    )

    my_db.session.add(new_word)
    my_db.session.commit()
    # save word,

    my_db.session.query(Words).delete()
    my_db.session.commit()
    # clear words data base,

    word=Saved.query.all()[-1].word

    response = request_handler(endpoint=endpoint,
                               app_key=app_key,
                               app_id=app_id,
                               language_code=language_code,
                               word=word)

    return render_template('index.html',
                           definitions=shorten_list(response['list_of_definitions']),
                           examples=shorten_list(response['list_of_examples']),
                           word_found=True,
                           message='Ah! Got it!',
                           save='saved')


@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register.html')


@app.route('/add-user', methods=['POST','GET'])
def add_user():
    # if request.method=='GET':
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if Users.query.filter_by(email=email).first():
        return 'email exists'
    hashed_password=generate_password_hash(password,
                                           method='pbkdf2:sha256',
                                           salt_length=8)
    new_user = Users(
        username=name,
        email=email,
        password=hashed_password
    )

    my_db.session.add(new_user)
    my_db.session.commit()

    login_user(new_user)

    return render_template('index.html', current_user=current_user)


@app.route('/login', methods=['POST','GET'])
def login():

    if request.method=='POST':
        entered_password=request.form.get('password')
        entered_email=request.form.get('email')

        user=Users.query.filter_by(email=entered_email).first()
        if not user:
            return 'no such email'

        if check_password_hash(user.password, entered_password):
            login_user(user)
            return render_template('index.html', current_user=current_user)
        else:
            return 'incorrect password'
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('choose', current_user=current_user))
    # return render_template('index.html',current_user=current_user)


@app.route('/favourites')
def favourite():
    have_favourites=True

    all_favourites=Saved.query.all()
    list_of_favourites=[]

    for word in all_favourites:
        list_of_favourites.append(word.word)
        # we build a list of words saved so far, and pass this list to index

    if not list_of_favourites:
        # if its empty,
        have_favourites=False

    return render_template('index.html', have_favourites=have_favourites, list_of_favourites=list_of_favourites)


@app.route('/favourite/<word>', methods=['POST', 'GET'])
def display_favourite(word):
    response = request_handler(endpoint=endpoint,
                               app_key=app_key,
                               app_id=app_id,
                               language_code=language_code,
                               word=word)
    # fetch word details through API request,
    # then pass result to index.html page,
    return render_template('index.html',
                           definitions=shorten_list(response['list_of_definitions']),
                           examples=shorten_list(response['list_of_examples']),
                           word_found=True,
                           message='Ah! Got it!',
                           save='saved')


@app.route('/test')
@login_required
def quiz():
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True)
