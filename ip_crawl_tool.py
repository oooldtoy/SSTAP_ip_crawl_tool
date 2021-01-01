# -*- coding: utf-8 -*-


import time,os
import config,udp,tcp,path_mod
import ctypes, sys,time



def run(exe_list):
    global udp_point,mode
    name_en = input('请输入游戏英文名（按回车跳过）：')
    name_zh = input('请输入游戏中文名（按回车默认为{}），注意！这将影响到SSTAP显示的名称！：'.format(str(exe_list)))
    if name_en == '':
        name_en = 'none'
    if name_zh == '':
        name_zh = str(exe_list)
    if len(exe_list) == 1:
        if mode == '1':
            rules_name = exe_list[0]+'_SSTAP'
        elif mode == '2':
            rules_name = exe_list[0]+'_NETCH'
    if len(exe_list) > 1:
        if mode == '1':
            rules_name = exe_list[0]+'...'+'_SSTAP'
        elif mode == '2':
            rules_name = exe_list[0]+'...'+'_NETCH'
    f = open('{}.rules'.format(rules_name), 'wb')
    if mode == '1':
        f.write('#{},{},0,0,1,0,1,0,By-ip_crawl_tool\n'.format(name_en,name_zh).encode())
    elif mode == '2':
        f.write('# {} {} By-ip_crawl_tool,1\n'.format(name_en,name_zh).encode())
    f.close()
    print('正在检测{}远程ip,可随时关闭窗口停止终止程序。\n现在你可以打开全局，并启动游戏，发现的ip将会自动记录到当前目录的rules文件中'.format(str(exe_list)))
    while True:
        
        time.sleep(0.2)#加入阻塞降低cpu占用
        ip_temp = tcp.tcp_crawl(exe_list)
        if ip_temp != []:
            for i in ip_temp:
                f_conf = open('config.txt','r+')
                ip_list = f_conf.read()
                if i not in ip_list:#:用于过滤重复ip
                    f_conf.close()
                    f_conf = open('config.txt','a')
                    f_conf.write(' '+i+' ')
                    f_conf.close()
                    f = open('{}.rules' .format(rules_name), 'ab+')
                    i = i.split('.')
                    i[3] = '0'
                    i = '.'.join(i)
                    f_conf = open('config.txt','r+')
                    ip_list = f_conf.read()
                    if i not in ip_list:#避免重复写入
                        f.write(i.encode() +b'/24\n')
                        f_conf.close()
                        f_conf = open('config.txt','a')
                        f_conf.write(' '+i+' ')
                        f_conf.close()
                    else:
                        f_conf.close()
                    f.close()
                else:
                    f_conf.close()
        if udp_point == 'udp':
            #print('正在检测udp')
            for i in udp.udp_crawl(exe_list):
                f_conf = open('config.txt','r+')
                ip_list = f_conf.read()
                if i not in ip_list:
                    f_conf.close()
                    f_conf = open('config.txt','a')
                    f_conf.write(' '+i+' ')
                    f_conf.close()
                    f = open('{}.rules' .format(rules_name), 'ab+')
                    i = i.split('.')
                    i[3] = '0'
                    i = '.'.join(i)
                    f_conf = open('config.txt','r+')
                    ip_list = f_conf.read()
                    if i not in ip_list:#避免重复写入
                        ip_temp.append(i)
                        f.write(i.encode() +b'/24\n')
                        f_conf.close()
                        f_conf = open('config.txt','a')
                        f_conf.write(' '+i+' ')
                        f_conf.close()
                    else:
                        f_conf.close()
                    f.close()
                else:
                    f_conf.close()

def is_admin():#确定管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main():
    #test()
    global udp_point,mode
    print('ip_crawl_tool'+config.version)
    f = open('config.txt','w')
    f.close()
    udp_point = input('是否抓取udp协议ip，默认不抓取。\n抓取udp协议ip需使用管理员权限运行，且需要开启windows防火墙，请确保使用管理员权限运行本程序和开启了防火墙。\n如需抓取udp协议请输入（udp）:')
    if udp_point == 'udp':
        if is_admin():
            pass
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)#获取管理员权限
            os._exit(0)
    while True:
        mode = input('请选择写入文件模式\n1.SSTAP\n2.NETCH。\n请输入1or2：')
        if mode == '1'or'2':
            break
    while True:
        input_mode = input('1.手动输入进程\n2.扫描文件夹\n请输入1or2：')
        if input_mode == '1':
            exe_list = input('请输入游戏进程名（可启动游戏后在任务管理器 “进程” 中查询）\n如果有多个进程请使用英文逗号分隔开：')
            exe_list = exe_list.split(',')
            break
        elif input_mode == '2':
            exe_path = input('请输入需要扫描的文件夹路径：')
            exe_list = path_mod.run(exe_path)
            break
        else:
            print('输入错误，请重新输入')
            continue


    print('将检测以下程序')
    for exe in exe_list:
        print(exe)
    print('请核对名称是否正确，如不正确请重新启动输入')
    run(exe_list)
    
if __name__ == '__main__':
    main()
    

