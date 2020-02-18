import os
from psutil import net_connections,Process,pids

#os.popen('firewall.cpl')
ip_list_udp = []

def search_pid(exe_list):#通过进程名查询pid
    pid_list = []
    a = pids()
    for i in a:
        try:
            #print(Process(i).name())
            if Process(i).name() in exe_list:
               pid_list.append(str(i))
               return pid_list
        except :
            continue
    

def udp_crawl(exe_list):
    a = os.popen('netsh firewall set logging %systemroot%\system32\LogFiles\Firewall\pfirewall.log 1024 ENABLE ENABLE')
    b = os.popen('type %systemroot%\system32\LogFiles\Firewall\pfirewall.log')
    port_list_1 = []#所选进程所占用端口
    port_list_0 = []#非所选进程占用端口
    
    pid_list = search_pid(exe_list)
    #print(pid_list)
    for i in b:
        #日志中寻找UDP记录
        if 'UDP' in i:
            j = i.split(' ')
            if ':' in j[5]:#去除ipv6
                continue
            if j[6] in port_list_0:
                continue
                for i_1 in os.popen('netstat -ano|findstr "'+j[6]+'"'):
                    #print(j[6])
                    #通过记录发现本地端口，并找到占用本地端口的PID
                    j_1 = i_1.split(' ')
                    j_1 = list(filter(None,j_1))#过滤空字符串
                    if j_1[3].replace('\n','') in pid_list:
                        port_list_1.append(j[6])
                        if j[5] not in ip_list_udp:
                            ip_list_udp.append(j[5])
                            print('发现新ip'+j[5]+'--udp')
                    else:
                        port_list_0.append(j[6])
            else:#去除重复的端口查询
                if j[5] not in ip_list_udp:
                    ip_list_udp.append(j[5])
                    print('发现新ip'+j[5]+'--udp')
    return ip_list_udp

if __name__ == '__main__':
    udp_crawl(['tcpudp_2.1.1.exe'])

