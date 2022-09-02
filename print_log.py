# -*- coding: utf-8 -*-
def print_log(text,is_print):
    if is_print == 1:
        print(text)
    elif is_print == 0:
        #print(text)
        f_log = open('log.txt', 'a')
        f_log.write(text+'\n')
        f_log.close()

