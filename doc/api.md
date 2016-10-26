# cloud_api云平台接口模块——接口定义

标签：云平台中可信OJ系统
---

## 说明

此为Restful风格的api，接受http的POST请求，参数需以表单的形式通过POST传入，返回结果为JSON。

服务url为`/cloud_api`，如果将其部署在本机上，则完整的地址为`127.0.0.1:5000/cloud_api`，其中url中的5000为python flask的默认服务端口，服务端口可修改，详见flask的文档。
POST的表单中的键值对中一定包含名称为`command`的键，指明具体调用什么服务。其他参数以键值对的形式存在于表单中。

返回的JSON的一般格式为：
``` JSON
{"return_code":return_code, "description":some_string}
```
return_code为返回码，description是对这次调用结果的描述。

---
## 返回值定义

说明：接口定义尚未固定，具体实现时的返回值及常见返回结果定义以`src/ret_code.py`为准。

| 名称  | 数值  |  描述  |
| --------   | ----- | ----  |
| RET_SUCCESS | 0 | 命令成功执行 |
| ERR_INVAL_CMD | 1 | 无效命令/POST表单中无command |
| ERR_ARG_MISSED | 2 | 参数缺失 |
| ERR_INVAL_IMAGE | 3 | 无效的镜像名/不存在名为此的镜像 |
| ERR_INVAL_FLAVOR | 4 | 无效的flavor/不存在名为此的flavor |
| ERR_INVAL_INTERNET | 5 | 是否允许虚拟机访问公网的值设置错误，取了`true`和`false`以外的值 |
| ERR_INVAL_VM_ID | 6 | 无效的虚拟机id | 
| ERR_INVAL_VM_CREATION_FAILURE | 7 | 虚拟机创建失败 |
| ERR_INVAL_CLOUD_CONFIG | 8 | 云平台配置存在错误，请联系云平台管理员更正 |

## API定义

### launch_instance

#### POST表单结构
| 键名    | 键值  |  描述  | 备注 |
| --------   | ----- | ----  | --- |
| command    | launch_instance |        |
|   image      |   xubuntu-14.04-desktop-x86   |   镜像名称   |  镜像名重复导致的结果尚未研究 |
|  flavor        |    m1.small |  虚拟机的配置选择  | flavor名重复导致导致的结果未研究 |
| internet | true/false | 是否允许虚拟机访问公网 | 为考生分配的虚拟机建议不允许公网访问，为老师分配的、用来安装软件的虚拟机建议允许公网访问 |
| name | final_exam_141242022 | 虚拟机名称 | 可重复，但建议选择考试名+考生学号的组合，这样当考试时出现问题时，可以第一时间从dashboard上处理 |

#### 返回值

* 成功
``` JSON
{
    'ret_code':RET_SUCCESS, 
    'description':'Success', 
    'vm_id':vm_id, 
    'vm_ip':vm_ip
}
```
说明：
1. `vm_id`可以唯一指定这个新建的虚拟机示例，后续对虚拟机的操作应根据对应的api要求，传入这个参数。
2. `vm_ip`即为虚拟机的ipv4地址，虚拟桌面客户端可通过这个ip地址连上虚拟桌面。

* 失败
``` JSON
{
    'ret_code':error_code, 
    'description':error_message
}
```

#### API实现状态
- [x] 实现
- [x] 单元测试
- [ ] 压力测试

### destroy_instance

#### POST表单结构
| 键名    | 键值  |  描述  | 备注 |
| --------   | ----- | ----  | --- |
| command | destroy_instance | 彻底销毁实例，释放所占有的资源，用于考生完成考试或老师装完软件并保存为新快照之后，销毁实例 |  |
| vm_id | XXXXXX-XXXXX | 虚拟机的id，即调用launch_instance时返回的id |

#### 返回值

* 成功
``` JSON
{
    'ret_code':RET_SUCCESS, 
    'description':'Success'
}
```

* 失败
``` JSON
{
    'ret_code':ERR_INVAL_VM_ID, 
    'description':'Invalid virtual machine id'
}
```
说明：其实即使vm_id无效，我们仍然可以返回成功，毕竟大不了什么都不干嘛。之所以要检测并捕获vm_id无效这个错误，是为了返回更多信息，方便OJ开发者捕获编程实现中的错误。

#### API实现状态
- [ ] 实现
- [ ] 单元测试
- [ ] 压力测试

