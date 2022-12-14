from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
import random
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import requests


def shorten_list(my_list):
    if len(my_list) <= 5:
        if len(my_list) == 0:
            my_list=['Sorry,Could not find one at the moment.'
                     'We definitely would soon']
            return my_list
        else:
            return my_list

    elif len(my_list) > 5:
        my_list=my_list[:5]
        return my_list


def request_handler(endpoint, language_code, word, app_id, app_key):
    """" function to handle API request, and build search result"""
    # it takes api credentials and search preferences as input,

    url = f"https://od-api.oxforddictionaries.com/api/v2/{endpoint}/{language_code}/{word.lower()}"

    word_definition_request = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    in_json = word_definition_request.json()

    list_of_definitions = []
    list_of_examples = []
    list_of_phrases = []

    # fill lists,
    if word_definition_request.status_code == 200:

        for search_result in in_json['results']:
            lexical_entries = search_result['lexicalEntries']
            for row in lexical_entries:
                entries = row['entries']
                for dictionary in entries:
                    senses = dictionary['senses']

                    try:
                        for each_sense_row in senses:
                            list_of_definitions.append(each_sense_row['definitions'][0])
                        for each_example_row in each_sense_row['examples']:
                            list_of_examples.append(each_example_row['text'])
                    except:
                        pass
                    else:
                        pass
    data={
        'list_of_definitions': list_of_definitions,
        'list_of_examples': list_of_examples,
    }

    return data

# api credentials
app_id = os.environ.get('dictionary_api_id')
app_key = os.environ.get('dictionary_api_key')
endpoint = "entries"

language_code = "en-us"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('web-dictionary-app-db-secret-key')
my_db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Users(my_db.Model , UserMixin):
    __tablename__='users'
    id = my_db.Column(Integer, primary_key=True)
    username = my_db.Column(String(80), nullable=False)
    email = my_db.Column(String(120), unique=True, nullable=False)
    password=my_db.Column(String(500), nullable=False)


class Words(my_db.Model, UserMixin):
    __tablename__='words'
    id=my_db.Column(Integer, primary_key=True)
    word=my_db.Column(String)


    # definitions=my_db.Column(String)
    # examples=my_db.Column(String)
    # saved=my_db.Column(String)


class Saved(my_db.Model, UserMixin):
    __tablename__='saved'
    id=my_db.Column(Integer, primary_key=True)
    word=my_db.Column(String)


class Deleted(my_db.Model, UserMixin):
    __tablename__='deleted'
    id=my_db.Column(Integer, primary_key=True)
    word=my_db.Column(String)


# my_db.drop_all()
# my_db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
def choose():
    # user either logs in or sign up,
    return render_template('index.html', current_user=False)


list_of_deleted = []


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

    saved_words = Saved.query.all()
    list_of_saved_words = []
    for row in saved_words:
        list_of_saved_words.append(row.word)

    if word in list_of_saved_words:
        # if word already exists in favo, don't display the add button,
        return render_template('index.html',
                               definitions=shorten_list(response['list_of_definitions']),
                               examples=shorten_list(response['list_of_examples']),
                               word_found=word,
                               message='Ah! Got it!',
                               save='saved')
    else:
        return render_template('index.html',
                               definitions=shorten_list(response['list_of_definitions']),
                               examples=shorten_list(response['list_of_examples']),
                               word_found=True,
                               message='Ah! Got it!',
                               )


@app.route('/save', methods=['POST', 'GET'])
def save():
    list_of_rows = Words.query.all()
    try:
        last_row = list_of_rows[-1]
    except IndexError:
        return 'index error'
    else:
        pass

    new_word = Saved(
        word=last_row.word
    )

    my_db.session.add(new_word)
    my_db.session.commit()
    # save word,

    my_db.session.query(Words).delete()
    my_db.session.commit()
    # clear words data base,

    word = Saved.query.all()[-1].word

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


@app.route('/add-user', methods=['POST', 'GET'])
def add_user():
    # if request.method=='GET':
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if Users.query.filter_by(email=email).first():
        flash('Email already in  use, login instead.', category='error')
        return render_template('login.html')
    hashed_password = generate_password_hash(password,
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


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        entered_password = request.form.get('password')
        entered_email = request.form.get('email')

        user = Users.query.filter_by(email=entered_email).first()
        if not user:
            flash("No such email, please register")
            return render_template('login.html')

        if check_password_hash(user.password, entered_password):
            login_user(user)
            return render_template('index.html', current_user=current_user)
        else:
            flash('Incorrect Password')
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('choose', current_user=current_user))
    # return render_template('index.html',current_user=current_user)


@app.route('/favourites')
def favourite():
    # global list_of_deleted
    have_favourites = True

    all_favourites = Saved.query.all()
    list_of_favourites = []
    for word in all_favourites:
        list_of_favourites.append(word.word)
        # we build a list of words saved so far, and pass this list to index

    deleted_words=Deleted.query.all()
    list_of_deleted_words=[]
    for row in deleted_words:
        list_of_deleted_words.append(row.word)

    for word in list_of_deleted_words:
        if word in list_of_favourites:
            list_of_favourites.remove(word)

    if not list_of_favourites:
        # if its empty,
        have_favourites = False

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


@app.route('/delete/<word>')
def delete_word(word):
    new_delete_entry=Deleted(
        word=word
    )

    my_db.session.add(new_delete_entry)
    my_db.session.commit()

    return quiz()


@app.route('/test')
@login_required
def quiz():
    saved_words = Saved.query.all()
    random_row = random.choice(saved_words)
    quiz_word = random_row.word

    deleted_words=Deleted.query.all()
    list_of_deleted_words=[]

    for row in deleted_words:
        list_of_deleted_words.append(row.word)

    start=True
    while start:
        if quiz_word in list_of_deleted_words:
            quiz_word=random.choice(saved_words).word
        else:
            start=False

    # make sure quiz word is not one of the deleted ones,
    response = request_handler(endpoint=endpoint,
                               app_key=app_key,
                               app_id=app_id,
                               language_code=language_code,
                               word=quiz_word)

    answer = shorten_list(response['list_of_definitions'])

    return render_template('index.html', quiz=quiz_word, answer=answer)


if __name__ == '__main__':
    app.run(debug=True)
