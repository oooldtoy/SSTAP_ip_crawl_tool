# -*- coding: utf-8 -*-

import os
import tkinter as tk

def print_log(text,is_print):#is_print为后台打印参数
    if is_print == 1:
        print(text)
        f_log = open('log.txt', 'a')
        f_log.write(text + '\n')
        f_log.close()
    elif is_print == 0:
        #print(text)
        f_log = open('log.txt', 'a')
        f_log.write(text+'\n')
        f_log.close()

def path_mod(path,exe_list):
    #exe_list = []
    for i in os.listdir(path):
        #print(path+i)
        if os.path.exists(path+'/'+i+'/'):#检测是否为文件夹
            path_mod(path+'/'+i+'/',exe_list)
        else:
            if i.endswith('.exe'):
                #print(i)
                exe_list.append(i)
    return exe_list

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))

        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

if __name__ == '__main__':
    print(path_mod('D:\TIM',[]))