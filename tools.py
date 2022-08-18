from main import *

def shorten_list(my_list):
    if len(my_list) in range(0, 5):
        pass
    else:
        my_list = my_list[:5]
        return my_list

