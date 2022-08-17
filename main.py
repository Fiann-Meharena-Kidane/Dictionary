from flask import Flask, render_template, redirect, request

import json
import requests
import os


app_id = os.environ.get('dictionary_api_id')
app_key = os.environ.get('dictionary_api_key')
endpoint = "entries"

# api credentials

language_code = "en-us"
word_id = "find"

# url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + word_id.lower()
# response = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})

# print(response.json())


app=Flask(__name__)


@app.route('/', methods=['POST','GET'])
def home():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    word=request.form.get('word')
    url=f"https://od-api.oxforddictionaries.com/api/v2/{endpoint}/{language_code}/{word.lower()}"
    word_definition_request=requests.get(url, headers = {"app_id": app_id, "app_key": app_key})
    in_json=word_definition_request.json()
    api_response=in_json['results'][0]['lexicalEntries'][0]['lexicalCategory']['text']

    return api_response

    # return word
    # return render_template('result.html', word=in_json)


if __name__=='__main__':
    app.run(debug=True)