# README

1. 配置好config.json

2. 执行如下脚本

```python
pip3 install aliyun-python-sdk-core
pip3 install aliyun-python-sdk-alidns
python3 run.py
```

## IP获取方式

目前使用[http://v4.ipv6-test.com/api/myip.php](http://v4.ipv6-test.com/api/myip.php)来获取IP地址，如果未来失效，可以采用如下其他几种获取方式：

* POST: [http://ip.taobao.com/service/getIpInfo.php?ip=myip](http://ip.taobao.com/service/getIpInfo.php?ip=myip)

* POST: [http://ip.taobao.com/service/getIpInfo2.php?ip=myip](http://ip.taobao.com/service/getIpInfo2.php?ip=myip)

* GET: [http://pv.sohu.com/cityjson](http://pv.sohu.com/cityjson)
