# 自动更新DNS解析（阿里云解析）

## 准备工作

1. 配置好config.json中的`access_key_id`和`access_key_secret`，可以在阿里云中找到，在`domains`中配置好需要批量更新解析的域名

## Linux服务器

1. 安装python3
2. 安装第三方库

    ```
    pip3 install aliyun-python-sdk-core
    pip3 install aliyun-python-sdk-alidns
    ```

3. 配置crontab定时脚本

## 群晖

1. 在群晖的套件中心中安装好python3
2. ssh进入群晖，通过`sudo -i`提升权限，并执行如下脚本（python3的安装目录会有些不同，需要改成你所设置的安装目录）：

    ```python
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    ln -s /volume3/@appstore/py3k/usr/local/bin/pip3 /usr/local/bin/pip3
    pip3 install aliyun-python-sdk-core
    pip3 install aliyun-python-sdk-alidns
    ```

3. 进入群晖“控制面板”->“任务计划”，配置好名字、执行时间、频率等，设置命令为如下代码（脚本目录需要改成你代码放置的目录）：

    ```python
    cd /volume3/scripts/ddns-for-alidns
    python3 run.py
    ```



## 外网IP获取方式

目前使用[http://v4.ipv6-test.com/api/myip.php](http://v4.ipv6-test.com/api/myip.php)来获取IP地址，未来如果失效，可以采用如下其他几种获取方式：

* POST: [http://ip.taobao.com/service/getIpInfo.php?ip=myip](http://ip.taobao.com/service/getIpInfo.php?ip=myip)

* POST: [http://ip.taobao.com/service/getIpInfo2.php?ip=myip](http://ip.taobao.com/service/getIpInfo2.php?ip=myip)

* GET: [http://pv.sohu.com/cityjson](http://pv.sohu.com/cityjson)
