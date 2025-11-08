# -*- coding: utf-8 -*-

import ip_crawl_tool
from mods import path_mod,createToolTip
from tkinter import Tk,Label,Entry,StringVar,Button,Checkbutton,Radiobutton,messagebox,scrolledtext
from tkinter.filedialog import askdirectory
import time,threading

exe_list = []
is_print = 0

def admin_info():
    if not ip_crawl_tool.is_admin():
        messagebox.showinfo(title='提示',message='抓取udp协议ip需使用管理员权限运行，且需要开启windows防火墙，请确保使用管理员权限运行本程序和开启了防火墙')

def selectpath():
    path = askdirectory()
    var_path.set(path)
def get_process():
    global exe_list
    path = e_path.get()
    if '/' in path:
        exe_list = path_mod(path,exe_list)
    else:
        exe_list = path.split(',')
    return exe_list

def insert_scrolledtext():

    text_all_1 = ''
    while True:
        time.sleep(2)
        f = open('log.txt', 'r')
        text_all = f.read()
        if text_all_1 != text_all:
            insert_text = text_all.replace(text_all_1, '')
            print_text.insert('end', insert_text)
            print_text.see('end')
        else:
            print_text.insert('end', '')
        text_all_1 = text_all
        #print_text.delete("1.0", "end")
        f.close()

def button():
    t1 = threading.Thread(target=ip_crawl_tool.run,args=(get_process(),udp_point.get(),mode.get(),e_name_en.get(),e_name_zh.get(),is_print))
    t1.setDaemon(True)
    t1.start()
    t2 = threading.Thread(target=insert_scrolledtext)
    t2.setDaemon(True)
    t2.start()

root = Tk()
var_path = StringVar()
udp_point = StringVar()
mode = StringVar()
mode.set('1')
Checkbutton_udp = Checkbutton(root, text = '抓取udp',variable = udp_point ,onvalue = 'udp', offvalue = '',command = admin_info)
Checkbutton_udp.place(x=20,y=30)
Label(root, text='选择模式').place(x=110,y=33)
r_sstapmode = Radiobutton(root,text = 'sstap',variable = mode,value='1')
r_netchmode = Radiobutton(root,text = 'netch',variable = mode,value='2')
r_sstapmode.place(x=160,y=20)
r_netchmode.place(x=160,y=40)
Label(root, text='填入游戏进程名或扫描的文件夹路径').place(x=20,y=80)
e_path = Entry(root, textvariable=var_path)
e_path.place(x=20,y=110,width=130,height=29)
createToolTip(e_path,'如果有多个进程请使用英文逗号分隔开')
b_path = Button(root, text='选择文件夹', command=selectpath)
b_path.place(x=150,y=110)
Label(root, text='请输入游戏英文名（可为空）').place(x=20,y=150)
e_name_en = Entry(root)
e_name_en.place(x=20,y=180,width=200,height=29)
Label(root, text='请输入游戏中文名,默认为进程名').place(x=20,y=220)
e_name_zh = Entry(root)
e_name_zh.place(x=20,y=250,width=200,height=29)
createToolTip(e_name_zh,'注意！这将影响到SSTAP显示的名称！')
b_start = Button(root, text='开始', command=button)
b_start.place(x=100,y=300)
print_text = scrolledtext.ScrolledText(root)
print_text.place(x=250,y=20,width=300,height=310)
root.geometry("560x350")
root.mainloop()

