# -*- coding: utf-8 -*-

import os
import tkinter as tk
from functools import reduce

#----------判断内网ip---------------#
def ip_into_int(ip):
    return reduce(lambda x,y:(x<<8)+y,map(int,ip.split('.')))

def is_internal_ip(ip):
    ip_int = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip_int >> 24 == net_a or ip_int >>20 == net_b or ip_int >> 16 == net_c
#----------判断内网ip---------------#

def print_log(log_message, enable_logging):#enable_logging为后台打印参数
    if enable_logging == 1:
        print(log_message)
        f_log = open('log.txt', 'a')
        f_log.write(log_message + '\n')
        f_log.close()
    elif enable_logging == 0:
        #print(log_message)
        f_log = open('log.txt', 'a')
        f_log.write(log_message+'\n')
        f_log.close()

def get_executables_in_dir(directory_path, process_list):
    #process_list = []
    for i in os.listdir(directory_path):
        #print(directory_path+i)
        if os.path.exists(directory_path+'/'+i+'/'):#检测是否为文件夹
            get_executables_in_dir(directory_path+'/'+i+'/', process_list)
        else:
            if i.endswith('.exe'):
                #print(i)
                process_list.append(i)
    return process_list

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

def create_tooltip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

if __name__ == '__main__':
    print(get_executables_in_dir('D:\TIM',[]))