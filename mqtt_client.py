import paho.mqtt.client as mqtt
import ssl
import time
import simplejson


# 获取当前系统时间
def cur_time():
    return int(time.time())


# 门锁上线
def device_online(client):
    time.sleep(1)
    topic_online = "/sys/2004747/thing/event/pushnotice"
    payload_online = {"msgId": "{}".format(cur_time()), "type": "online", "notice": {"deviceId": "2012638"}}
    client.publish(topic=topic_online, payload=simplejson.dumps(payload_online))


# 发送下拉消息
def device_msgnotice(client):
    time.sleep(1)
    topic_msgnotice = "/sys/2004747/thing/event/notify"
    payload_msgnotice = {"displayType": "txt", "fromId": "2012638", "message": "yourenyongshoujikaimen",
                         "msgId": "{}".format(cur_time()), "notifyType": "deviceinfo",
                         "showLocation": "log,notification,alert"}
    client.publish(topic=topic_msgnotice, payload=simplejson.dumps(payload_msgnotice))


def main():
    # 创建mqtt客户端，并设置设备id
    client = mqtt.Client(client_id="c78c3d44ddec47ecbe9e232cca7c145d")
    # 配置客户端参数
    client.tls_set(ca_certs=r'F:\Practice\python workspace\code_test\mqtt_test\PortalCA.crt', certfile=None,
                   keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    # 配置服务器证书中服务器主机名的验证
    client.tls_insecure_set(True)
    # 连接服务端
    client.connect("192.168.1.101", 1883, 5)
    device_online(client)
    device_msgnotice(client)
    # 断开连接
    client.disconnect()


if __name__ == '__main__':
    main()
