import json
from linkkit import linkkit
import time
import shared

ProductKey = "k1h41jOvnlr"
DeviceName = "shumeipai"
DeviceSecret = "4884f6cedfd6bd78cc3e3b046b56a4b6"

def on_connect(session_flag, rc, userdata):
    print("on_connect:%d, rc:%d, userdata:" % (session_flag, rc))
#连接返回处理函数
def on_disconnect(rc, userdata):
    print("on_disconnect: rc:%d, userdata:" % rc)
#取消连接返回处理函数
def on_subscribe_topic(mid, granted_qos, userdata):
    print("on_subscribe_topic mid:%d, granted_qos:%s" % (mid, str(','.join('%s' % it for it in granted_qos))))
#订阅主题返回处理函数
def on_topic_message(topic, payload, qos, userdata):
    print("Received message from topic:", topic)
    data = json.loads(payload)
    if "items" in data and "Lock" in data["items"]:
        shared.lock_value = data["items"]["Lock"]["value"]
        #print("Lock value:", shared.lock_value)
    if "items" in data and "password" in data["items"]:
        shared.true_password = data["items"]["password"]["value"]
        print("password:", shared.true_password)
#接收消息返回处理函数
def on_unsubscribe_topic(mid, userdata):
    print("on_unsubscribe_topic mid:%d" % mid)
#取消订阅主题返回处理函数
def on_publish_topic(mid, userdata):
    print("on_publish_topic mid:%d" % mid)
#发送数据返回处理函数
def on_thing_enable(self, userdata):
        print("on_thing_enable")

def on_thing_disable(self, userdata):
        print("on_thing_disable")

def on_thing_prop_post(self, request_id, code, data, message,userdata):
        print("on_thing_prop_post request id:%s, code:%d, data:%s message:%s" %
              (request_id, code, str(data), message))
#发送数据处理函数
'''
    lk = linkkit.LinkKit(
        host_name="cn-shanghai",
        product_key=ProductKey,
        device_name=DeviceName,
        device_secret=DeviceSecret
    )
'''
'''
lk.thing_setup("lock.json")
lk.on_connect = on_connect
lk.on_disconnect = on_disconnect
lk.on_subscribe_topic = on_subscribe_topic
lk.on_topic_message = on_topic_message
lk.on_publish_topic = on_publish_topic
lk.on_unsubscribe_topic = on_unsubscribe_topic

lk.connect_async()
time.sleep(2)

# Subscribe to the topic where you expect to receive messages
rc, mid = lk.subscribe_topic(lk.to_full_topic("/k1h41jOvnlr/shumeipai/user/get"))

# Publish example data to a topic
while True:
    rc, mid = lk.publish_topic(lk.to_full_topic("/sys/{}/thing/event/property/post".format(ProductKey)), json.dumps(payload_json))
    time.sleep(2)
'''
