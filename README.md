# 自动更新DNS解析（阿里云解析）

## 配置说明

1. 配置好config.json中的`access_key_id`和`access_key_secret`，可以在阿里云中找到
2. 在`domains`中配置好需要批量更新解析的域名

## 外网IP获取方式

目前使用[http://v4.ipv6-test.com/api/myip.php](http://v4.ipv6-test.com/api/myip.php)来获取IP地址，未来如果失效，可以采用如下其他几种获取方式：

* POST: [http://ip.taobao.com/service/getIpInfo.php?ip=myip](http://ip.taobao.com/service/getIpInfo.php?ip=myip)

* POST: [http://ip.taobao.com/service/getIpInfo2.php?ip=myip](http://ip.taobao.com/service/getIpInfo2.php?ip=myip)

* GET: [http://pv.sohu.com/cityjson](http://pv.sohu.com/cityjson)
