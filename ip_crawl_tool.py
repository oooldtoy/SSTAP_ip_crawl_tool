# -*- coding: utf-8 -*-

import os
import config,udp,tcp
import ctypes,sys,time
from mods import print_log, get_executables_in_dir
from tempfile import NamedTemporaryFile

def run(process_list, is_udp_enabled, output_mode, english_name, chinese_name, enable_logging):
    print(output_mode, english_name, chinese_name)
    
    # 重置log文件
    with open('log.txt', 'w') as f_log:
        pass
        
    if english_name == '':
        english_name = 'none'
    if chinese_name == '':
        chinese_name = str(process_list)
        
    if len(process_list) == 1:
        if output_mode == '1':
            rules_filename = process_list[0] + '_SSTAP'
        elif output_mode == '2':
            rules_filename = process_list[0] + '_NETCH'
    elif len(process_list) > 1:
        if output_mode == '1':
            rules_filename = process_list[0] + '...' + '_SSTAP'
        elif output_mode == '2':
            rules_filename = process_list[0] + '...' + '_NETCH'
            
    with open('{}.rules'.format(rules_filename), 'wb') as f:
        if output_mode == '1':
            f.write('#{},{},0,0,1,0,1,0,By-ip_crawl_tool\n'.format(english_name, chinese_name).encode())
        elif output_mode == '2':
            f.write('# {} {} By-ip_crawl_tool,1\n'.format(english_name, chinese_name).encode())
            
    print_log(','.join(process_list), enable_logging)
    print_log('正在检测{}远程ip,可随时关闭窗口停止终止程序。\n现在你可以打开全局，并启动游戏，发现的ip将会自动记录到当前目录的rules文件中'.format(str(process_list)), enable_logging)
    
    seen_ips = set()
    seen_subnets = set()
    
    while True:
        time.sleep(0.2) # 加入阻塞降低cpu占用
        
        # TCP 检测
        found_tcp_ips = tcp.tcp_crawl(process_list, enable_logging, seen_ips)
        if found_tcp_ips:
            with open('{}.rules'.format(rules_filename), 'ab+') as f:
                for ip in found_tcp_ips:
                    parts = ip.split('.')
                    parts[3] = '0'
                    subnet = '.'.join(parts)
                    if subnet not in seen_subnets:
                        seen_subnets.add(subnet)
                        f.write(subnet.encode() + b'/24\n')
                        
        # UDP 检测
        if is_udp_enabled == 'udp':
            found_udp_ips = udp.udp_crawl(process_list, enable_logging, seen_ips)
            if found_udp_ips:
                with open('{}.rules'.format(rules_filename), 'ab+') as f:
                    for ip in found_udp_ips:
                        parts = ip.split('.')
                        parts[3] = '0'
                        subnet = '.'.join(parts)
                        if subnet not in seen_subnets:
                            seen_subnets.add(subnet)
                            f.write(subnet.encode() + b'/24\n')

def is_admin():#确定管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    enable_logging = 1
    print('ip_crawl_tool'+config.version)
    
    if is_admin():
        print('\n[状态] 当前已获取管理员权限。')
    else:
        print('\n[状态] 当前为普通用户权限 (抓取UDP将会自动申请提权)。')
        
    if len(sys.argv) > 1 and sys.argv[1] == 'udp_auto':
        udp_mode = 'udp'
        print('\n已自动选择抓取UDP协议 (提权后继承选项)。\n')
    else:
        udp_mode = input('是否抓取udp协议ip，默认不抓取。\n抓取udp协议ip需使用管理员权限运行，且需要开启windows防火墙，请确保使用管理员权限运行本程序和开启了防火墙。\n如需抓取udp协议请输入（udp）:')
        
    if udp_mode == 'udp':
        if is_admin():
            pass
        else:
            if getattr(sys, 'frozen', False):
                exe_path = sys.executable
                params = 'udp_auto'
            else:
                exe_path = sys.executable
                params = f'"{__file__}" udp_auto'
            ctypes.windll.shell32.ShellExecuteW(None, "runas", exe_path, params, None, 1)#获取管理员权限
            os._exit(0)
            
    while True:
        output_mode = input('请选择写入文件模式\n1.SSTAP\n2.NETCH。\n请输入1or2：')
        if output_mode in ['1', '2']:
            break
    while True:
        input_method = input('1.手动输入进程\n2.扫描文件夹\n请输入1or2：')
        if input_method == '1':
            process_list_str = input('请输入游戏进程名（可启动游戏后在任务管理器 “进程” 中查询）\n如果有多个进程请使用英文逗号分隔开：')
            process_list = process_list_str.split(',')
            break
        elif input_method == '2':
            directory_path = input('请输入需要扫描的文件夹路径：')
            process_list = get_executables_in_dir(directory_path, process_list=[])
            break
        else:
            print('输入错误，请重新输入')
            continue
    print('将检测以下程序')
    for exe in process_list:
        print(exe)
    print('请核对名称是否正确，如不正确请重新启动输入')
    english_name = input('请输入游戏英文名（按回车跳过）：')
    chinese_name = input('请输入游戏中文名（按回车默认为{}），注意！这将影响到SSTAP显示的名称！：'.format(str(process_list)))
    run(process_list, udp_mode, output_mode, english_name, chinese_name, enable_logging)
    
if __name__ == '__main__':
    main()
