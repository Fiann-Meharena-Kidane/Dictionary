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


