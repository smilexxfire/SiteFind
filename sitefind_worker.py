# -*- coding: UTF-8 -*-
'''
@Project ：SiteFind 
@File    ：sitefind_worker.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/9/11 17:14 
@Comment ： 
'''
import json
from common.database.consumer import RabbitMQConsumer
from modules.sitefind import httpx

class SitefindWorker(RabbitMQConsumer):
    def __init__(self, queue_name):
        super().__init__(queue_name)

    def task_handle(self):
        task = json.loads(self.message)
        # 获取targets
        targets = task['targets']
        task_id = task['task_id']
        httpx.run(targets, task_id)

if __name__ == '__main__':
    # 启动子域名扫描服务
    worker = SitefindWorker("sitefind")
    worker.start_consuming()