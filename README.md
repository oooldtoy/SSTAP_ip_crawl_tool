# SSTAP_ip_crawl_tool
一个自动获取游戏远程ip，并自动写成SSTAP规则文件的脚本。

此脚本由python3编写，测试过的版本为3.6，3.7，3.8，其他版本未验证（理论上3.0以上都没问题）。

依赖的第三方库为

客户端（SSTAP_ip_crawl_tool.py）psutil;<br>



使用方法：
-------
启动程序(ip_crawl_tool.py或者ip_crawl_tool.v***.exe)后输入需要抓取IP的程序名，然后根据提示输入游戏英文名、中文名随即进入抓取状态。

进入抓取状态后开启SSTAP全局进入游戏即可自动抓取ip并填写入规则文件。

获取到ip后关闭窗口即可退出程序。

为确保获取规则的完整性，务必保证多运行几分钟（也就是开着全局和工具多玩一会）

规则文件在程序当前目录中。

**请注意：3.3.3版本后，增加的udp协议抓取，需打开windows防火墙，然后使用管理员权限运行程序（主要是为了能够打开和读取防火墙日志）。**

不会python可以选择下载release中打包好的exe可执行文件https://github.com/oooldtoy/SSTAP_ip_crawl_tool/releases/download/v4.0/ip_crawl_tool.v4.0.exe




更新说明：
-------
v4.0<br>
1.删除上传服务器功能<br>
2.增加netch模式<br>
3.增加文件夹选择模式<br>
v3.4<br>
1.修复报错bug<br>
2.修复抓取到内网ip和包丢ip的bug<br>
v3.3.6<br>
1.修复ip分享<br>
v3.3.5（已删除，bug待修复）<br>
1.bug修复<br>
2.增加udp从属进程显示<br>
v3.3.4<br>
1.bug修复<br>
v3.3.3<br>
1.增加udp协议ip抓取<br>
v3.2<br>
1.修复ipv6过滤<br>
2.增加进程名和版本号上传<br>
3.修改文件命名逻辑<br>
v3.1<br>
1.增加web端管理员页面<br>
2.所有配置信息转移至config.py<br>
3.修复某些环境下运行打包的exe文件报错问题<br>
v3.0.1<br>
1.修复SSTAP代理下无法进行上传规则的bug<br>
2.隐藏网页端ip后两位<br>
3.增加客户端连接和连接失败的提示<br>
4.修改说明

v3.0<br>
1.增加自动上传规则功能<br>
2.增加快速规则预览网页服务<br>
3.修复ipv6规则相关问题

v2.0<br>
1.更新同时抓取多个进程的功能<br>
2.更新规则写入模式，使其覆盖IP段更加全面

关于如何获取程序名称：
-------

首先打开游戏，然后打开任务管理器，找到游戏进程

![查找程序名第一步](https://raw.githubusercontent.com/oooldtoy/SSTAP_ip_crawl_tool/master/MD_IMG/1.png)

然后右键点击该进程属性

![查找程序名第二步](https://raw.githubusercontent.com/oooldtoy/SSTAP_ip_crawl_tool/master/MD_IMG/2.png)

然后在红框位置的即为程序名称：

![查找程序名第三步](https://raw.githubusercontent.com/oooldtoy/SSTAP_ip_crawl_tool/master/MD_IMG/3.png)

![查找程序名总览](https://raw.githubusercontent.com/oooldtoy/SSTAP_ip_crawl_tool/master/MD_IMG/4.png)
