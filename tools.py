from main import *


def shorten_list(my_list):
    if len(my_list) in range(0, 5):
        if len(my_list) == 0:
            my_list=['Sorry,Could not find one at the moment.'
                     'We definitely would soon']
            return my_list
        pass
    else:
        my_list = my_list[:5]
        return my_list
