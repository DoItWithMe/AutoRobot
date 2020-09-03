import json
import requests
import socket
import time
import datetime
import redis
from apscheduler.schedulers.background import BackgroundScheduler
#from multiprocess import Process


def serviceServer(server):
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 10086
    ip = "0.0.0.0"
    server.bind((ip, port))
    server.listen(5)
    print("Service server start success.")


def regitsterService(scheduler, jsonData):
    webhook = jsonData['webhook']
    message = jsonData['message']
    if len(webhook) == 0:
        return -1
    if len(message) == 0:
        return -1

    # 解析时间
    task_time = datetime.datetime.strptime(jsonData['time'], "%Y-%m-%d %H:%M:%S")

    scheduler.add_job(messagePush, 'date', run_date=task_time, args=[webhook, message])
    print(message)
    return 0


def messagePush(webhook, message):
    header = {'Content-Type': 'application/json'}
    requests.post(webhook, data=json.dumps(message), params=header)


def schedulerService():
    scheduler = BackgroundScheduler()
    scheduler.start()
    # 创建注册服务监听
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serviceServer(server)

    # 不断的去监听，是否有新任务需要注册
    while True:
        result = -1
        # 获取body
        client, addr = server.accept()
        body = client.recv(1024).decode('utf-8').split('\r\n\r\n', 1)[1]
        print(body)
        try:
            jsonData = json.loads(body)
            print(jsonData)
            result = regitsterService(scheduler, jsonData)
        except:
            result = -1

        # 返回注册者是否注册成功
        if result == 0:
            response = json.dumps({'status': 'OK'}).encode('utf-8')
            client.send(response)
        else:
            response = json.dumps({'status': 'FAILED'}).encode('utf-8')
            client.send(response)
        client.close()
        time.sleep(1)


if __name__ == '__main__':
    schedulerService()
