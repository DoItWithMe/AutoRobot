# AutoRobot

调用wechat work的机器人API，自动推送消息

# 注册发送任务

```
curl 'http://127.0.0.1:10086'\
  -H 'Content-Type: application/json' \
  -d '{
    "webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxxxxxxxx",
    "time": "2020-09-03 10:37:00",
    "message": {
      "msgtype": "text",
      "text": {
        "content": "今天我请大家吃饭",
        "mentioned_mobile_list": ["phone_number"]
      }
    }
  }'
```
