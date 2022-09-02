# -*- coding: utf-8 -*-
import os

exe_list = []

def run(path):
    for i in os.listdir(path):
        #print(path+i)
        if os.path.exists(path+'/'+i+'/'):#检测是否为文件夹
            run(path+'/'+i+'/')
        else:
            if i.endswith('.exe'):
                #print(i)
                exe_list.append(i)
    return exe_list

    
if __name__ == '__main__':                
    print(run('E:/OneDrive/PycharmProjects/'))
