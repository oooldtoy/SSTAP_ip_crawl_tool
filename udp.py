# -*- coding: utf-8 -*-
import os
from psutil import net_connections,Process,pids
from functools import reduce
from print_log import print_log

#----------判断内网ip---------------#

def ip_into_int(ip):
    return reduce(lambda x,y:(x<<8)+y,map(int,ip.split('.')))

def is_internal_ip(ip):
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c

#----------判断内网ip---------------#

#os.popen('firewall.cpl')
ip_list_udp = []
pid_list = []
pid_dist = {}#进程名对应pid列表
def search_pid(exe_list):#通过进程名查询pid
    for exe in exe_list:
        pid_dist[exe] = []
    a = pids()
    for i in a:
        try:
            #print(Process(i).name())
            if Process(i).name() in exe_list:
                for exe in exe_list:
                    if Process(i).name() == exe:
                        pid_dist[exe].append(i)
                pid_list.append(str(i))
        except :
            continue
    return pid_list
    

def udp_crawl(exe_list,is_print):
    os.popen('netsh firewall set logging %systemroot%\system32\LogFiles\Firewall\pfirewall.log 1024 ENABLE ENABLE')
    log = os.popen('type %systemroot%\system32\LogFiles\Firewall\pfirewall.log')
    port_list_1 = []#所选进程所占用端口
    port_list_0 = []#非所选进程占用端口
    
    pid_list = search_pid(exe_list)
    #print(pid_list)
    for each_logline in log:
        #日志中寻找UDP记录
        if 'UDP' in each_logline:
            log_list = each_logline.split(' ')
            if ':' in log_list[5]:#去除ipv6
                continue
            try:
                if log_list[6] in port_list_0:#重复非占用端口直接跳过
                    continue
            except IndexError:
                continue
            for i in os.popen('netstat -ano|findstr "'+log_list[6]+'"'):
                #print(log_list[6])
                #通过记录发现本地端口，并找到占用本地端口的PID
                j = i.split(' ')
                j = list(filter(None,j))#过滤空字符串
                if j[3].replace('\n','') in pid_list:
                    port_list_1.append(log_list[6])
                    if log_list[5] not in ip_list_udp:
                        for exe in pid_dist:
                            if j[3].replace('\n','') in pid_dist[exe]:#获取ip从属进程
                                exe = exe
                                break
                        if is_internal_ip(log_list[5]) != True and log_list[5].split('.')[0] !='127':
                            f_conf = open('temp.txt','r')
                            ip_list = f_conf.read()
                            if log_list[5] not in ip_list:
                                ip_list_udp.append(log_list[5])
                                print_log('发现新ip '+exe+'--udp\n'+log_list[5],is_print)
                            f_conf.close()
                else:
                    port_list_0.append(log_list[6])
    #print(len(ip_list_udp))
    return ip_list_udp

if __name__ == '__main__':
    #print(search_pid(['aria2c.exe','dlpc.exe','chrome.exe']))
    #print(pid_dist)
    udp_crawl(['aria2c.exe'])
