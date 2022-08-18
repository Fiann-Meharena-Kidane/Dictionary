from flask import Flask, render_template, redirect, request

from tools import *
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


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html', message="Welcome!")


@app.route('/result', methods=['GET', 'POST'])
def result():
    word = request.form.get('word')
    url = f"https://od-api.oxforddictionaries.com/api/v2/{endpoint}/{language_code}/{word.lower()}"
    word_definition_request = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    in_json = word_definition_request.json()
    # api_response=in_json['results'][0]['lexicalEntries']
    api_response = in_json
    list_of_definitions = []
    list_of_examples = []
    list_of_phrases = []

    # fill lists,
    # definitions.append(in_json['results'][0]['lexicalEntries'][1])

    if word_definition_request.status_code == 200:

        for search_result in in_json['results']:
            entries_dictionary = search_result['lexicalEntries']
            for value in entries_dictionary:
                entries = value['entries']
                for dictionary in entries:
                    senses = dictionary['senses']

                    # definitions
                    for senses_dictionary in senses:
                        # list_of_definitions.append(senses_dictionary['definitions'])

                        try:
                            list_of_definitions.append(senses_dictionary['definitions'][0])
                        except:
                            return 'something went wrong'

                        else:
                            # list_of_definitions.append(row['definitions'])
                            list_of_definitions.append(senses_dictionary['definitions'][0])

                        # examples ...
                        try:
                            list_of_examples_raw = senses_dictionary['examples']
                        except:
                            list_of_examples = []
                        else:
                            for example in list_of_examples_raw:
                                list_of_examples.append(example['text'])

                        # list_of_examples.append(row['examples'][0]['text'])
    else:
        return render_template('index.html', message="Sorry, we could not find that word")

    print(list_of_definitions)
    print(list_of_examples)

    return render_template('index.html',
                           definitions=shorten_list(list_of_definitions),
                           examples=shorten_list(list_of_examples),
                           word_found=True,
                           message='Ah! Got it!')


if __name__ == '__main__':
    app.run(debug=True)
