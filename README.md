# 自动更新DNS解析（阿里云解析）

## 准备工作

1. 配置好config.json中的`access_key_id`和`access_key_secret`，可以在阿里云中找到，在`domains`中配置好需要批量更新解析的域名

## Linux服务器

1. 安装python3
2. 安装第三方库

    ```
    pip3 install -r requirements.txt
    ```

3. 配置crontab定时脚本

## 群晖

1. 进入群晖“控制面板”->“任务计划”，新增一个“触发的任务”，事件是“开机”，执行以下脚本，目的是安装依赖库，并且防止系统更新后库丢失：

    ```bash
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple aliyun-python-sdk-core
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple aliyun-python-sdk-alidns
    ```

2. 进入群晖“控制面板”->“任务计划”，配置好名字、执行时间、频率等，设置命令为如下代码（脚本目录需要改成你代码放置的目录）：

    ```bash
    cd /volume3/scripts/ddns-for-alidns
    python3 main.py
    ```



## 外网IP获取方式

目前使用[http://v4.ipv6-test.com/api/myip.php](http://v4.ipv6-test.com/api/myip.php)来获取IP地址，未来如果失效，可以采用如下其他几种获取方式：

* POST: [http://ip.taobao.com/service/getIpInfo.php?ip=myip](http://ip.taobao.com/service/getIpInfo.php?ip=myip)

* POST: [http://ip.taobao.com/service/getIpInfo2.php?ip=myip](http://ip.taobao.com/service/getIpInfo2.php?ip=myip)

* GET: [http://pv.sohu.com/cityjson](http://pv.sohu.com/cityjson)
