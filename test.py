# from main import requests, app_id, app_key, language_code, endpoint
#
# word='put'
# url = f"https://od-api.oxforddictionaries.com/api/v2/{endpoint}/{language_code}/{word.lower()}"
# word_definition_request = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
#
# print(word_definition_request.json())

demo=['the place where one lives permanently, especially as a member of a family or household', 'an institution for people needing professional care or supervision', '(in sports) the goal or end point', 'relating to the place where one lives', "(of a sports game) played at the team's own field or court", 'denoting the administrative center of an organization', 'to or at the place where one lives', '(of an animal) return by instinct to its territory after leaving it', 'move or be aimed toward (a target or destination) with great accuracy']

print(len(demo))


# def shorten_list(my_list):
#     if len(my_list) < 5:
#         if len(my_list) == 0:
#             my_list=['Sorry,Could not find one at the moment.'
#                      'We definitely would soon']
#             return my_list
#     elif len(my_list) > 5:
#         my_list=my_list[:5]
#         return my_list
#     else:
#         return my_list


# print(shorten_list(demo))
# print(len(shorten_list(demo)))
#

# print(len(demo))
#
# print(len(demo) in range(0,5))
# print(result)

from main import *

def handle_login():
    if request.method == 'POST':
        entered_password = request.form.get('password')
        entered_email = request.form.get('email')
        user = Users.query.filter_by(email=entered_email).first()
        print(user.password)

        if check_password_hash(user.password, entered_password):
            login_user(user)
            return render_template('index.html', current_user=current_user)
        else:
            return 'incorrect password'
    else:
        return render_template('login.html')

#
# print(response.json())

# import json
# import requests
# import os
#
# app_id  = os.environ.get('dictionary_api_id')
# app_key = os.environ.get('dictionary_api_key')
# endpoint = "entries"
# language_code = "en-us"
# word_id = "find"
#
#
#
# #
# # print("code {}\n".format(r.status_code))
# # print("text \n" + r.text)
# # print("json \n" + json.dumps(r.json()))
#
# dictionary={'name':'fiann', 'age':12, 'address':'dc'}
#
# for value in dictionary:
#     print('hey')
#
# print(len(dictionary))
#


# list=[1,2,3,4,5,6]
#
#
# if len(list) in range(0,5):
#     print('it is less than 5')
# else:
#     print('it is not less than 5')
#     list=list[:5]
#
#

# if len() in counter:
#     print("it is less than 5")
#     max=max(list)
#     print(max)

