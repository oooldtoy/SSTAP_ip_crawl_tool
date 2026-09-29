# -*- coding: utf-8 -*-
import os
import subprocess
import psutil
from mods import print_log, is_internal_ip

pid_map = {} # 进程名对应pid列表
udp_ip_list = []

def find_pids_by_name(process_list): #通过进程名查询pid
    active_pids = []
    pid_map.clear()
    for exe in process_list:
        pid_map[exe] = []
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name']
            if name in process_list:
                pid_str = str(proc.info['pid'])
                pid_map[name].append(pid_str)
                active_pids.append(pid_str)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return active_pids

def udp_crawl(process_list, enable_logging, seen_ips):
    subprocess.run(['netsh', 'firewall', 'set', 'logging', r'%systemroot%\system32\LogFiles\Firewall\pfirewall.log', '1024', 'ENABLE', 'ENABLE'], capture_output=True, shell=True)
    
    log_path = os.path.expandvars(r'%systemroot%\system32\LogFiles\Firewall\pfirewall.log')
    try:
        with open(log_path, 'r', encoding='ansi', errors='ignore') as f:
            log = f.readlines()
    except IOError:
        print_log('无法读取防火墙日志，请确保拥有管理员权限', enable_logging)
        return []

    active_pids = find_pids_by_name(process_list)
    
    # 建立当前系统全部 UDP 本地端口到 PID 的映射字典
    port_to_pid = {}
    for conn in psutil.net_connections('udp'):
        if conn.pid is not None and conn.laddr:
            port_to_pid[str(conn.laddr.port)] = str(conn.pid)
            
    found_ips = []
    
    for log_line in log:
        if 'UDP' in log_line:
            log_parts = log_line.split(' ')
            if len(log_parts) < 7:
                continue
                
            remote_ip = log_parts[5]
            local_port = log_parts[6]
            
            if ':' in remote_ip: #去除ipv6
                continue
                
            pid = port_to_pid.get(local_port)
            if pid and pid in active_pids:
                process_name = "unknown"
                for exe in pid_map:
                    if pid in pid_map[exe]: #获取ip从属进程
                        process_name = exe
                        break
                
                if not is_internal_ip(remote_ip) and not remote_ip.startswith('127.'):
                    if remote_ip not in seen_ips:
                        seen_ips.add(remote_ip)
                        found_ips.append(remote_ip)
                        print_log(f'发现新ip {process_name}--udp\n{remote_ip}', enable_logging)
                        
    return found_ips

if __name__ == '__main__':
    udp_crawl(['aria2c.exe'], 1, set())
