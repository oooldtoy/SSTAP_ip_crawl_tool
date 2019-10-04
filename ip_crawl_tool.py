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

def run(name):
    print('按下Ctrl+C停止')
    name_en = input('请输入游戏英文名（按回车跳过）：')
    name_zh = input('请输入游戏中文名（按回车默认为{}）：'.format(name))
    if name_en == '':
        name_en = 'none'
    if name_zh == '':
        name_zh == name
    f = open('{}.rules'.format(name), 'wb')
    f.write('#{},{},0,0,1,0,1,0,By-ip_crawl_tool\n'.format(name_en,name_zh).encode())
    f.close()
    ip_list = []
    print('正在检测{}远程ip,可随时按下Ctrl+C停止终止程序。\n现在你可以打开SSTAP全局，并启动游戏，发现的ip将会自动记录到当前目录的rules文件中'.format(name))
    while True:
        ip_temp = search(name)
        if ip_temp != []:
            for i in ip_temp:
                if i not in ip_list:
                    ip_list.append(i)
                    print('发现新ip')
                    print(i)
                    f = open('{}.rules' .format(name), 'ab+')
                    if i.endswith('.0'):
                        f.write(i.encode()+b'/24\n')
                    if i.endswith('.0.0'):
                        f.write(i.encode()+b'/16\n')
                    else:
                        f.write(i.encode() +b'/32\n')
                    f.close()


if __name__ == '__main__':
    #print(search('dlpc.exe'))
    #test()
    #run('dlpc.exe')
    a = input('请输入游戏进程名（可启动游戏后在任务管理器 进程 中查询）：')
    run(a)