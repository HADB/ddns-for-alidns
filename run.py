# -*- coding: utf-8 -*-

import json
import logging
from aliyunsdkcore import client
from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
from aliyunsdkalidns.request.v20150109 import (AddDomainRecordRequest, DescribeDomainRecordsRequest, UpdateDomainRecordRequest)
from logging.handlers import TimedRotatingFileHandler
from socket import error as SocketError
from socket import timeout as SocketTimeout
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


# 获取配置
def get_config():
    with open('config.json') as config_file:
        config = json.load(config_file)
        return config


# 从域名中获取RR和主域名
def get_domain_parts(domain):
    parts = domain.split('.')
    length = len(parts)
    if length > 2:
        return '.'.join(parts[0:length - 2]), '.'.join(parts[length - 2:length])
    else:
        return '@', '.'.join(parts[0:length])


# 获取解析记录
def get_record(acs_client, domain_name, rr):
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(domain_name)
    request.set_accept_format('json')
    records = json.JSONDecoder().decode(acs_client.do_action_with_exception(request).decode())['DomainRecords']['Record']
    for record in records:
        if record['RR'] == rr:
            return record['RecordId'], record['Value']
    return None, None


# 添加记录
def add_record(acs_client, record_id, rr, domain_name, current_ip, ttl):
    request = AddDomainRecordRequest.AddDomainRecordRequest()
    request.set_RR(rr)
    request.set_Type('A')
    request.set_DomainName(domain_name)
    request.set_Value(current_ip)
    request.set_TTL(ttl)
    request.set_accept_format('json')
    result = acs_client.do_action_with_exception(request)
    return result


# 更新记录
def update_record(acs_client, record_id, rr, domain_name, current_ip, ttl):
    request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    request.set_RR(rr)
    request.set_Type('A')
    request.set_Value(current_ip)
    request.set_RecordId(record_id)
    request.set_TTL(ttl)
    request.set_accept_format('json')
    result = acs_client.do_action_with_exception(request)
    return result


# 获取外网IP
def get_public_ip():
    return urlopen('http://v4.ipv6-test.com/api/myip.php', timeout=10).read().decode()


# 主函数
def main():
    handler = TimedRotatingFileHandler('logs/ddns-for-alidns', when='midnight', interval=1, backupCount=0, encoding='utf-8')
    handler.suffix = '%Y%m%d.log'
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    config = get_config()
    acs_client = client.AcsClient(config['access_key_id'], config['access_key_secret'], config['region_id'])
    try:
        current_ip = get_public_ip()
        for domain in config['domains']:
            rr, domain_name = get_domain_parts(domain)
            record_id, value = get_record(acs_client, domain_name, rr)
            if record_id == None:
                add_record(acs_client, record_id, rr, domain_name, current_ip, config['ttl'])
                logging.info(domain + '添加解析为' + current_ip)
            else:
                if value != current_ip:
                    update_record(acs_client, record_id, rr, domain_name, current_ip, config['ttl'])
                    logging.info(domain + '更新解析为' + current_ip)
        logger.info('SUCCESS')
    except HTTPError as e:
        logger.error('http error: ' + str(e.code) + ': ' + str(e.reason))
        return 0
    except URLError as e:
        logger.error('url error: ' + str(e.reason))
        return 0
    except SocketTimeout:
        logger.error('socket timed out')
        return 0
    except SocketError as e:
        logger.error('socket error: ' + str(e))
        return 0
    except ClientException as e:
        logger.error('aliyun client error: ' + str(e.error_code) + ': ' + str(e.message))
        return 0
    except ServerException as e:
        logger.error('aliyun server error: ' + str(e.error_code) + ': ' + str(e.message))
        return 0
    except:
        logger.error('其他异常')
        raise


if __name__ == '__main__':
    main()
