# -*- coding: utf-8 -*-
import psutil
from os.path import basename
from psutil import net_connections, Process
from mods import print_log, is_internal_ip

def tcp_crawl(process_list, enable_logging, seen_ips):
    found_ips = []
    for process_name in process_list:
        for conn in net_connections('tcp'):
            laddr, raddr, status, pid = conn[3:]
            if not raddr or pid is None:
                continue
            try:
                process_filename = basename(Process(pid).exe())
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            else:
                if process_filename == process_name:
                    if raddr.ip != '127.0.0.1' and ':' not in raddr.ip: # 判断是否为本机地址以及剔除ipv6
                        if not is_internal_ip(raddr.ip): # 判断是否为内网ip
                            if raddr.ip not in seen_ips:
                                seen_ips.add(raddr.ip)
                                found_ips.append(raddr.ip)
                                print_log('发现新ip {}--tcp'.format(process_name), enable_logging)
                                print_log(raddr.ip, enable_logging)
    return found_ips

if __name__ == '__main__':
    print(is_internal_ip('28.32.9.1'))
