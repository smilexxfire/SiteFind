# -*- coding: UTF-8 -*-
'''
@Project ：SiteFind 
@File    ：httpx.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/9/11 2:38 
@Comment ： 
'''
import json
import os
import subprocess
from common.module import Module
from config.log import logger
class Httpx(Module):
    def __init__(self, targets:list):
        self.modules = "sitefind"
        self.source ="httpx"
        self.collection = "sitefind"
        self.targets = targets
        Module.__init__(self)

    def do_scan(self):
        cmd = [self.execute_path, "-l", self.targets_file, "-random-agent", "-j", "-o", self.result_file]
        subprocess.run(cmd)

    def deal_data(self):
        logger.log("INFOR", "Start deal data process")
        if not os.path.exists(self.result_file):
            return
        with open(self.result_file, "r", encoding="utf8") as f:
            datas = f.readlines()
            json_list = [json.loads(data) for data in datas]
            for data in json_list:
                data.setdefault("resolvers", None)
                del data["resolvers"]
                data.setdefault("a", None)
                data.setdefault("aaaa", None)
                data.setdefault("cname", None)
                del data["cname"]
                del data["a"]
                del data["aaaa"]
            self.results = json_list
    def save_db(self):
        # print(self.results)
        super().save_db()

    def run(self):
        self.begin()
        self.save_targets()
        self.do_scan()
        self.deal_data()
        self.save_db()
        self.finish()
        self.delete_temp()

def run(targets:list):
    httpx = Httpx(targets)
    httpx.run()

if __name__ == '__main__':
    run(["qiniu.xxf.world:80","me.xxf.world:443", "www.baidu.com:443"])