from os.path import basename
from psutil import net_connections,Process
from functools import reduce
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

def tcp_crawl(exe_list):
    ip_temp = []
    for name in exe_list:
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
                    if raddr.ip != '127.0.0.1' and ':' not in raddr.ip:#判断是否为本机地址以及剔除ipv6
                        if is_internal_ip(raddr.ip) != True:#判断是否为内网ip
                            f_conf = open('config.txt','r')
                            ip_list = f_conf.read()
                            if raddr.ip not in ip_list:
                                ip_temp.append(raddr.ip)
                                print('发现新ip {}--tcp'.format(name))
                                print(raddr.ip)
                            f_conf.close()
    return(ip_temp)

if __name__ == '__main__':
    print(is_internal_ip('28.32.9.1'))

