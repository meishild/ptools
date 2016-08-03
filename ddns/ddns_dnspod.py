# -*- coding:utf8 -*-
# !/usr/bin/env python2

# author          :haiyang.song
# email           :meishild@gmail.com
# datetime        :16/7/21
# version         :1.0
# python_version  :2.7.7
# description     :
# ==============================================================================
import ConfigParser
import httplib
import json
import os
import urllib
import socket
import sys
import time

from log_config import logger


class DDNSLoader:
    def __init__(self):
        self._domain_id = None
        self._current_ip = None
        self._record_dict = {}
        self._config = None
        self._login_token = None
        self.load_config()
        self._is_alive = True

    def load_config(self):
        path = os.path.split(os.path.realpath(__file__))[0] + '/config.cnf'
        self._config = ConfigParser.ConfigParser()
        if not os.path.exists(path):
            print "配置文件不存在!!!"
            sys.exit()
        self._config.read(path)
        self._login_token = ("%s,%s" % (self._config.get("dnspod", "id"), self._config.get("dnspod", "token")))

    def post_json(self, req_api, params):
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
        conn = httplib.HTTPSConnection(self._config.get("dnspod", "host"))
        conn.request("POST", req_api, urllib.urlencode(params), headers)
        response = conn.getresponse()
        date = response.read()
        return dict(
            status=response.status,
            reason=response.reason,
            json=json.loads(date)
        )

    def get_domain(self):
        if self._domain_id is not None:
            return

        response = self.post_json("/Domain.List", dict(
            login_token=self._login_token,
            format="json"
        ))
        assert response['status'] == 200
        if "domains" not in response['json']:
            logger.error(u"[DNSPOD]登陆异常:" + response['json']['status']['message'])
            return

        domains = response['json']['domains']
        if len(domains) < 1:
            logger.error("[DNSPOD]没有域名配置,请先在dnspod配置域名")
            return

        for domain_dict in response['json']['domains']:
            if self._config.get("config", "domain") == domain_dict['punycode']:
                self._domain_id = domain_dict['id']

    def get_ip(self):
        sock = socket.create_connection(('ns1.dnspod.net', 6666), 20)
        ip = sock.recv(16)
        sock.close()
        return ip

    def get_record(self):
        response = self.post_json("/Record.List", dict(
            login_token=self._login_token,
            format="json",
            domain_id=self._domain_id
        ))
        assert response['status'] == 200
        for record in response['json']['records']:
            if record['type'] == 'A' and record['name'] in self._config.get("config", "sub_domain").split(","):
                self._record_dict[record['name']] = record

    def ddns(self, ip, record_id, sub_domain):
        response = self.post_json("/Record.Ddns", dict(
            login_token=self._login_token,
            format="json",
            domain_id=self._domain_id,
            ip=ip,
            record_id=record_id,
            sub_domain=sub_domain,
            record_line="默认",
        ))
        return response['status'] == 200

    def start(self):
        while self._is_alive:
            try:
                if self._domain_id is None:
                    self.get_domain()
                if len(self._record_dict) == 0:
                    self.get_record()

                ip = self.get_ip()
                logger.info("LOCAL IP ADDR:" + ip)
                if self._current_ip != ip:
                    for sub_domain, record in self._record_dict.items():
                        if ip == record['value']:
                            continue
                        if self.ddns(ip, record['id'], sub_domain):
                            self._current_ip = ip
                            logger.info("[DNSPOD]CHANGE %s DDNS IP [%s --> %s]" % (sub_domain, current_ip, ip))
                        else:
                            logger.info("[DNSPOD]REFRESH DDNS FAIL")
            except Exception as e:
                logger.error(e)
            time.sleep(30)

    def stop(self):
        self._is_alive = False


if __name__ == '__main__':
    DDNSLoader().start()
