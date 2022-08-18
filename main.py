from flask import Flask, render_template, redirect, request

from tools import *
import json
import requests
import os

# api credentials
app_id = os.environ.get('dictionary_api_id')
app_key = os.environ.get('dictionary_api_key')
endpoint = "entries"


language_code = "en-us"

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html', message="Welcome!")


@app.route('/result', methods=['GET', 'POST'])
def result():
    word = request.form.get('word')
    response=request_handler(endpoint=endpoint,
                            app_key=app_key,
                            app_id=app_id,
                            language_code=language_code,
                            word=word)

    return render_template('index.html',
                           definitions=shorten_list(response['list_of_definitions']),
                           examples=shorten_list(response['list_of_examples']),
                           word_found=True,
                           message='Ah! Got it!')


if __name__ == '__main__':
    app.run(debug=True)
