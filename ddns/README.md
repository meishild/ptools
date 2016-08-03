# dnspot动态DDNS
1.dnspot绑定域名解析。
2.用户中心-->安全设置 开启api token
3.配置config.cnf

* 安装windows服务
依赖

[python2.7](https://www.python.org/downloads/release/python-2712/)
[pywin32](https://sourceforge.net/projects/pywin32/)

* 安装windows服务
ddns目录位置随意但是注册以后不要修改。

安装服务
python win_service.py install 

安装并自动启动
python win_service.py --startup auto install 

启动服务
python win_service.py start

重启服务
python win_service.py restart

停止服务
python win_service.py stop

删除/卸载服务
python win_service.py remove

