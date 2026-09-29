# -*- coding: utf-8 -*-

import ip_crawl_tool
from mods import get_executables_in_dir, create_tooltip
from tkinter import Tk, Label, Entry, StringVar, Button, Checkbutton, Radiobutton, messagebox, scrolledtext
from tkinter.filedialog import askdirectory
import time, threading
import sys, os, ctypes

process_list = []
enable_logging = 0

def check_admin_privileges():
    if udp_var.get() == 'udp' and not ip_crawl_tool.is_admin():
        res = messagebox.askyesno(title='提权提示', message='抓取UDP协议需要管理员权限，当前为普通权限。\n是否立即重新以管理员身份运行本程序？\n(注意：这会重新启动界面，未保存的输入将丢失)')
        if res:
            if getattr(sys, 'frozen', False):
                exe_path = sys.executable
                params = 'udp_auto'
            else:
                exe_path = sys.executable
                params = f'"{__file__}" udp_auto'
            
            ctypes.windll.shell32.ShellExecuteW(None, "runas", exe_path, params, None, 1)
            os._exit(0)
        else:
            udp_var.set('')

def select_directory():
    path = askdirectory()
    path_var.set(path)

def get_process_list():
    global process_list
    path = path_entry.get()
    if '/' in path:
        process_list = get_executables_in_dir(path, process_list)
    else:
        process_list = path.split(',')
    return process_list

last_log_size = 0

def check_log():
    global last_log_size
    try:
        with open('log.txt', 'r', errors='ignore') as f:
            f.seek(last_log_size)
            new_text = f.read()
            if new_text:
                log_text_widget.insert('end', new_text)
                log_text_widget.see('end')
            last_log_size = f.tell()
    except FileNotFoundError:
        pass
    root.after(2000, check_log)

def start_crawling():
    worker_thread = threading.Thread(target=ip_crawl_tool.run, args=(get_process_list(), udp_var.get(), output_mode_var.get(), en_name_entry.get(), zh_name_entry.get(), enable_logging))
    worker_thread.daemon = True
    worker_thread.start()
    # 使用 tkinter 线程安全的 after() 方法在主线程轮询日志
    check_log()

root = Tk()

if ip_crawl_tool.is_admin():
    root.title("SSTAP_ip_crawl_tool [管理员]")
else:
    root.title("SSTAP_ip_crawl_tool [普通权限]")

path_var = StringVar()
udp_var = StringVar()

if len(sys.argv) > 1 and sys.argv[1] == 'udp_auto':
    udp_var.set('udp')

output_mode_var = StringVar()
output_mode_var.set('1')
udp_checkbutton = Checkbutton(root, text='抓取udp', variable=udp_var, onvalue='udp', offvalue='', command=check_admin_privileges)
udp_checkbutton.place(x=20, y=30)
Label(root, text='选择模式').place(x=110, y=33)
sstap_radio = Radiobutton(root, text='sstap', variable=output_mode_var, value='1')
netch_radio = Radiobutton(root, text='netch', variable=output_mode_var, value='2')
sstap_radio.place(x=160, y=20)
netch_radio.place(x=160, y=40)
Label(root, text='填入游戏进程名或扫描的文件夹路径').place(x=20, y=80)
path_entry = Entry(root, textvariable=path_var)
path_entry.place(x=20, y=110, width=130, height=29)
create_tooltip(path_entry, '如果有多个进程请使用英文逗号分隔开')
path_select_button = Button(root, text='选择文件夹', command=select_directory)
path_select_button.place(x=150, y=110)
Label(root, text='请输入游戏英文名（可为空）').place(x=20, y=150)
en_name_entry = Entry(root)
en_name_entry.place(x=20, y=180, width=200, height=29)
Label(root, text='请输入游戏中文名,默认为进程名').place(x=20, y=220)
zh_name_entry = Entry(root)
zh_name_entry.place(x=20, y=250, width=200, height=29)
create_tooltip(zh_name_entry, '注意！这将影响到SSTAP显示的名称！')
start_button = Button(root, text='开始', command=start_crawling)
start_button.place(x=100, y=300)
log_text_widget = scrolledtext.ScrolledText(root)
log_text_widget.place(x=250, y=20, width=300, height=310)
root.geometry("560x350")
root.mainloop()
