# -*- coding: UTF-8 -*-
'''
@Project ：SiteFind 
@File    ：mysitefind.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/9/11 17:23 
@Comment ： 
'''
from common.database.db import conn_db

class MySiteFind(object):
    def __init__(self):
        self.ip_port_cache = {}

    def get_subdomains_from_domain(self, domain):
        db = conn_db("subdomain")
        subdomains = db.find({"domain": domain})
        subdomain_values = [doc.get("subdomain") for doc in subdomains]
        return subdomain_values

    def get_subdomains_from_assert(self, assert_name):
        db = conn_db("asserts")
        # 第一步：在 asserts 集合中根据 assert_name 查找所有文档
        assert_docs = db.find({"assert_name": assert_name})
        # 提取所有的 domain 字段
        domains = [doc.get("domain") for doc in assert_docs if doc.get("domain")]
        if not domains:
            return f"No documents found with assert_name: {assert_name} or no domain fields."
        db = conn_db("subdomain")
        # 第二步：在 subdomain 集合中查找所有与 domain 匹配的 subdomain
        subdomains = db.find({"domain": {"$in": domains}})
        # 提取 subdomain 值
        subdomain_values = [doc.get("subdomain") for doc in subdomains]
        return subdomain_values

    def get_ips_from_domain(self, domain):
        subdomains = self.get_subdomains_from_domain(domain)
        db = conn_db("dns_record")
        ips = db.find({"domain": {"$in": subdomains}})
        ips_values = [value for doc in ips for value in doc.get("a", [])]
        return list(set(ips_values))

    def get_ips_from_assert(self, assert_name):
        subdomains = self.get_subdomains_from_assert(assert_name)
        db = conn_db("dns_record")
        ips = db.find({"domain": {"$in": subdomains}})
        ips_values = [value for doc in ips for value in doc.get("a", [])]
        return list(set(ips_values))

    def get_open_ports_from_ip_with_naabu(self, ip):
        if self.ip_port_cache.get(ip):
            return self.ip_port_cache[ip]
        db = conn_db("portscan_naabu")
        query = {"host": ip}
        document = db.find_one(query)
        # 获取开放的端口
        if document:
            open_ports = document['open_ports'] if 'open_ports' in document else []
            self.ip_port_cache[ip] = open_ports
            return open_ports
        return []

    def get_open_ports_from_subdomain_with_naabu(self, subdomain):
        db = conn_db("dns_record")
        query = {"domain": subdomain}
        document = db.find_one(query)
        all_ports = []
        if document is not None:
            a_field_value = document['a'] if 'a' in document else []
            # 可能有多个v4地址
            for a in a_field_value:
                open_ports = self.get_open_ports_from_ip_with_naabu(a)
                all_ports.extend(open_ports)
        return list(set(all_ports))

    def get_site_find_targets_from_domain_with_naabu(self, domain):
        '''
        domain获取所有subdomain，subdomain解析的ip，结合naabu扫描结果获取开放的端口组成target

        :param domain:
        :return:
        '''
        res = []
        # 获取ip:port格式
        ips = self.get_ips_from_domain(domain)
        ips = list(set(ips))
        for ip in ips:
            open_ports = self.get_open_ports_from_ip_with_naabu(ip)
            for port in open_ports:
                print(f"{ip}:{port}")
                res.append(f"{ip}:{port}")
        # 获取subdomain:port格式
        subdomains = self.get_subdomains_from_domain(domain)
        for subdomain in subdomains:
            all_ports = self.get_open_ports_from_subdomain_with_naabu(subdomain)
            for port in all_ports:
                print(f"{subdomain}:{port}")
                res.append(f"{subdomain}:{port}")

        return list(set(res))

if __name__ == '__main__':
    mysitefind = MySiteFind()
    print(mysitefind.get_site_find_targets_from_domain_with_naabu("tuchong.com"))