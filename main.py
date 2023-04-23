# -*- coding: utf-8 -*-
import json
import time
from urllib.request import urlopen

from aliyunsdkalidns.request.v20150109 import (
    AddDomainRecordRequest,
    DescribeDomainRecordsRequest,
    UpdateDomainRecordRequest,
)
from aliyunsdkcore import client
from yuanfen import logger
from yuanfen.config import Config

config = Config("config.json")


# 从域名中获取RR和主域名
def get_domain_parts(domain):
    parts = domain.split(".")
    length = len(parts)
    if length > 2:
        return ".".join(parts[0 : length - 2]), ".".join(parts[length - 2 : length])
    else:
        return "@", ".".join(parts[0:length])


# 获取解析记录
def get_record(acs_client, domain_name, rr):
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(domain_name)
    request.set_accept_format("json")
    records = json.JSONDecoder().decode(acs_client.do_action_with_exception(request).decode())["DomainRecords"][
        "Record"
    ]
    for record in records:
        if record["RR"] == rr and record["Type"] == "A":
            return record["RecordId"], record["Value"], record["TTL"]
    return None, None, None


# 添加记录
def add_record(acs_client, record_id, rr, domain_name, current_ip, ttl):
    request = AddDomainRecordRequest.AddDomainRecordRequest()
    request.set_RR(rr)
    request.set_Type("A")
    request.set_DomainName(domain_name)
    request.set_Value(current_ip)
    request.set_TTL(ttl)
    request.set_accept_format("json")
    result = acs_client.do_action_with_exception(request)
    return result


# 更新记录
def update_record(acs_client, record_id, rr, domain_name, current_ip, ttl):
    request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    request.set_RR(rr)
    request.set_Type("A")
    request.set_Value(current_ip)
    request.set_RecordId(record_id)
    request.set_TTL(ttl)
    request.set_accept_format("json")
    result = acs_client.do_action_with_exception(request)
    return result


# 获取外网IP
def get_public_ip():
    return urlopen("http://v4.ipv6-test.com/api/myip.php", timeout=10).read().decode()


# 主函数
def run():
    try:
        acs_client = client.AcsClient(config["access_key_id"], config["access_key_secret"], config["region_id"])
        current_ip = get_public_ip()

        for domain_config in config["domains"]:
            domain = domain_config["domain"]
            config_ttl = domain_config["ttl"]
            try:
                rr, domain_name = get_domain_parts(domain)
                record_id, record_ip, record_ttl = get_record(acs_client, domain_name, rr)
                if record_id == None:
                    add_record(acs_client, record_id, rr, domain_name, current_ip, config_ttl)
                    logger.info(f"{domain} 添加解析:{current_ip}, TTL:{config_ttl}")
                elif record_ip != current_ip or record_ttl != config_ttl:
                    update_record(acs_client, record_id, rr, domain_name, current_ip, config_ttl)
                    logger.info(f"{domain} 更新解析:{current_ip}, TTL:{config_ttl}")

            except Exception as e:
                logger.error(f"{domain} {str(e)}")

        logger.debug("SUCCESS")

    except Exception as e:
        logger.error(f"GLOBAL {str(e)}")


if __name__ == "__main__":
    while True:
        run()
        time.sleep(60)
