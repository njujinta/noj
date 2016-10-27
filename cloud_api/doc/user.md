# cloud_api云平台接口模块——安装及使用手册

---

## 安装

说明：建议在ubuntu 14.04及以上版本上安装，以下指令在ubuntu 16.04 LTS上测试通过

1. 安装python-novaclient-6.0.0
`pip install python-novaclient=6.0.0`
安装完成后运行`nova --version`或`/usr/local/bin/nova --version`，确保安装的是6.0.0版本。
采用`sudo apt-get install python-novaclient`安装的是较老的包，会导致有些API无法正常使用。

2. 安装python flask框架
`pip install flask`

---

##配置及启动服务

1. openstack的配置（allen：这里待完善）

2. 启动服务
将oj用户的openstack rc文件移入src文件夹下，运行`./run.sh your_rc_file`
