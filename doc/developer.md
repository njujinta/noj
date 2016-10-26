# cloud_api云平台接口模块——开发者手册

---

## 环境配置

1. 请阅读用户手册的`安装`这一节，确保安装好python-novaclient及flask框架

2. 安装httpie(供调试用)
`pip instal httpie`

---

## 基础知识及资源

1. 了解http协议并学习简单使用python flask框架
请简要阅读廖雪峰python教程的[web开发](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832648091917b035146084c43b05754ec9408dfaf000)这一章。

2. [novaclient 6.0.0的文档](http://docs.openstack.org/developer/python-novaclient/index.html)以及(openstack上的user guide)[http://docs.openstack.org/user-guide/sdk.html]

3. httpie的使用
只要学会发送表单，命令格式十分简单 
``` shell
http -f POST 127.0.0.1:5000/cloud_api command=launch_instance image_id=XXXXX flavor_id=XXXX allow_internet_access=XXXXX
```
其中`-f`选项表示我们是要发送一个form，而POST指明了方法为POST，后面是url，及一系列表单中的键值对。

4. 熟练使用python
推荐[廖雪峰的python教程](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000)

---

## 开发流程

1. fork这个项目（我不是来骗fork的，只是我以为只有fork之后才可以提pull request，如有新方法，请务必告知我）

2. 阅读doc/api.md查看有没有尚未实现的api

3. 实现
参考src/cloud_api.py中已有的其他api的实现，实现这个api(即增加一个函数，函数名与api名称相同)

4. 测试
运行`./run.sh your_openstack_rc_file`启动服务器，使用httpie发送http请求，查看返回结果是否符合api定义。
同时在dashboard上查看操作是否正确执行。但要注意的是，在负载较大时，操作的延迟可能较大。
测试用例请以shell脚本的格式放入test目录下，命名为test_api.sh，其中api为对应api的名称。

5. 发出pull request，请求merge进master
现阶段，该项目的主要开发及维护者为allen。请发出pull请求，维护者在review完代码后会选择性地并入master。在成功提交若干次后，将有机会加入这个项目，获得直接提交merge进master的资格。

---

## 调试建议

### 常见的http错误与可能的问题

1. `500 Internal Server Error` 
这是我们的web服务器出了内部错误，多半是编程错误，在启动服务器的终端中可以看到stack trace，由此定位错误。

2. `400 Bad Request`
一般是由于发送请求的表单没填好，缺少某些值，例如发送这个http请求 
``` shell
http -f POST 127.0.0.1:5000/cloud_api mad=miao
```
在cloud_api.py中利用`request.form['command']`访问command键值时就会出错，最终导致400错误。

3. `200 OK`
服务器正确响应。

### 测试

1. 每当在函数中新调用了一个api，务必用httpie进行测试，观察其会抛出哪些异常，是否被正常捕获，捕获之后的处理逻辑是否有问题等。
2. 在测试时，应时刻关注dashboard上的内容，看看操作是否产生结果。同时应注意，有些操作很慢，有可能要好几秒才能有结果，记得时常刷新dashboard。在测试结束后，请在dashboard上检查资源分配情况，将测试产生的没用的虚拟机，无用的floating_ip等，并及时回收。

---

## openstack api使用注意点

1. openstack官网上的document可能不太完整，太过简洁，参数表都没描述清楚。这个时候我们可以上网google，最靠谱的方法是拿pdb跟踪一下，找到对应的库的原文件，简单看一下函数定义。
2. 我本来是想使用最新的openstacksdk中的api的，它接口统一且规范。但是由于sdk的实现似乎还有一些问题，同时我在测试api时也遭遇到了一些暂时无法解决的问题，只能使用每个project自己的sdk，主要用到了novaclient及keystoneclient的sdk。我们使用的都是v2的api。
