# -*- coding: utf-8 -*-

from os.path import basename
from psutil import net_connections,Process


def test():
    for conn in net_connections('all'):
        laddr,raddr,status,pid = conn[3:]
        if not raddr:
            continue
        try:
            filename = basename(Process(pid).exe())
        except:
            pass
        else:
            msg = '''程序文件名：{}\n本地地址：{}\n远程地址：{}\n连接状态：{}'''.format(filename,laddr,raddr,status)
            print(msg)


def search(name):
    ip_temp = []
    for conn in net_connections('all'):
        laddr, raddr, status, pid = conn[3:]
        if not raddr:
            continue
        try:
            filename = basename(Process(pid).exe())
        except:
            pass
        else:
            if filename == name:
                #print('远程地址：'+str(raddr))
                if raddr.ip != '127.0.0.1':
                    ip_temp.append(raddr.ip)
    return ip_temp

def run(exe_list):
    name_en = input('请输入游戏英文名（按回车跳过）：')
    name_zh = input('请输入游戏中文名（按回车默认为{}），注意！这将影响到SSTAP显示的名称！：'.format(str(exe_list)))
    if name_en == '':
        name_en = 'none'
    if name_zh == '':
        name_zh = str(exe_list)
    f = open('{}.rules'.format(str(exe_list)), 'wb')
    f.write('#{},{},0,0,1,0,1,0,By-ip_crawl_tool\n'.format(name_en,name_zh).encode())
    f.close()
    ip_list = []
    print('正在检测{}远程ip,可随时关闭窗口停止终止程序。\n现在你可以打开SSTAP全局，并启动游戏，发现的ip将会自动记录到当前目录的rules文件中'.format(str(exe_list)))
    while True:
        for name in exe_list:
            ip_temp = search(name)
            if ip_temp != []:
                for i in ip_temp:
                    if i not in ip_list:
                        ip_list.append(i)
                        print('发现{}新ip'.format(name))
                        print(i)
                        f = open('{}.rules' .format(str(exe_list)), 'ab+')
                        if ':' in i:
                            f.write(i.encode()+b'/32\n')
                        else:
                            i = i.split('.')
                            i[3] = '0'
                            i = '.'.join(i)
                            if i not in ip_list:#避免重复写入
                                f.write(i.encode() +b'/24\n')
                                ip_list.append(i)
                        f.close()


if __name__ == '__main__':
    #test()
    a = input('请输入游戏进程名（可启动游戏后在任务管理器 进程 中查询）\n如果有多个进程请使用英文逗号分隔开：')
    exe_list = a.split(',')
    print('将检测以下程序')
    for exe in exe_list:
        print(exe)
    print('请核对名称是否正确，如不正确请重新启动输入')
    run(exe_list)
