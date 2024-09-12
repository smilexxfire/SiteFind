# -*- coding: UTF-8 -*-
'''
@Project ：SiteFind 
@File    ：producer.py
@IDE     ：PyCharm 
@Author  ：smilexxfire
@Email   : xxf.world@gmail.com
@Date    ：2024/9/11 17:20 
@Comment ： 
'''
import json

from common.database.producer import RabbitMQProducer
from modules.mysitefind import MySiteFind


QUEUE_NAME = "sitefind"
def purge_queue():
    """
    清空队列

    :param queue_name: 队列名称
    :return:
    """
    producer = RabbitMQProducer(QUEUE_NAME)
    producer.purge_queue()

def send_task(task):
    producer = RabbitMQProducer(QUEUE_NAME)
    producer.publish_message(json.dumps(task))

def send_site_find_task_from_domain(domain):
    '''
    通过主域名发送站点发现任务

    :param domain: 主域名
    :return:
    '''
    mysitefind = MySiteFind()
    targets = mysitefind.get_site_find_targets_from_domain_with_naabu(domain)
    print(targets)
    batch_size = 100
    # 使用循环和切片来分批处理列表
    for i in range(0, len(targets), batch_size):
        # 获取当前批次的数据
        batch = targets[i:i + batch_size]
        task = {
            "module": "httpx",
            "targets": batch
        }
        send_task(task)


if __name__ == '__main__':
    send_site_find_task_from_domain("tuchong.com")