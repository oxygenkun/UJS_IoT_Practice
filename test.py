import json
import logging
import random
import time

from linkkit import linkkit

LOG_FORMAT = "%(thread)d %(asctime)s  %(levelname)s %(filename)s %(lineno)d %(message)s"
DATE_FORMAT = "%m/%d/%Y-%H:%M:%S-%p"
logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT)
# 读取相关配置：HostName 、ProductKey 、DeviceName 、DeviceSecret
with open('config.json', 'r') as f:
    conf = json.load(f)
HostName = conf['HostName']
ProductKey = conf['ProductKey']
DeviceName = conf['DeviceName']
DeviceSecret = conf['DeviceSecret']  # 一机一密
lk = linkkit.LinkKit(
    host_name=HostName,
    product_key=ProductKey,
    device_name=DeviceName,
    device_secret=DeviceSecret  # 一机一密
)


# 连接
def on_connect(session_flag, rc, userdata):
    logging.info("on_connect:%d,rc:%d,userdata:" % (session_flag, rc))


# 断开连接
def on_disconnect(rc, userdata):
    logging.info("on_disconnect:rc:%d,userdata:" % rc)


# 订阅
def on_subscribe_topic(mid, granted_qos, userdata):
    logging.info("on_subscribe_topic mid:%d, granted_qos:%s" %
                 (mid, str(','.join('%s' % it for it in granted_qos))))


# 取消订阅
def on_unsubscribe_topic(mid, userdata):
    logging.info("on_unsubscribe_topic mid:%d" % mid)


# Topic消息
def on_topic_message(topic, payload, qos, userdata):
    logging.info("on_topic_message:" + topic + " payload:" + str(payload) + " qos:" + str(qos))


# 发布消息
def on_publish_topic(mid, userdata):
    logging.info("on_publish_topic mid:%d" % mid)


# 上报属性
def on_thing_prop_post(request_id, code, data, message, userdata):
    logging.info("on_thing_prop_post request id:%s, code:%d message:%s, data:%s,userdata:%s" %
                 (request_id, code, message, data, userdata))


# 云端设置本地端属性
def on_thing_prop_changed(message, userdata):
    if "PowerSwitch" in message.keys():
        prop_data["PowerSwitch"] = message["PowerSwitch"]
    elif "WindSpeed" in message.keys():
        prop_data["WindSpeed"] = message["WindSpeed"]
    elif "WorkMode" in message.keys():
        prop_data["WorkMode"] = message["WorkMode"]
    else:
        logging.warning("wrong data:%s" % message)
    lk.thing_post_property(message)  # SDK不会主动上报属性变化，如需要修改后再次上报云端，需要调用thing_post_property()发送
    print('prop_data:', prop_data)
    print('message:', message)
    logging.info("on_thing_prop_changed  data:%s " % message)


# 用户可以进行属性上报，事件上报，服务响应，此调用需要在连接前
def on_thing_enable(userdata):
    logging.info("on_thing_enable")


def on_thing_disable(self, userdata):
    print("on_thing_disable")


#
def on_thing_call_service(identifier, request_id, params, userdata):
    logging.info("on_thing_call_service")


# 服务端对上报的事件处理后发出响应
def on_thing_event_post(self, event, request_id, code, data, message, userdata):
    logging.info(
        "on_thing_event_post event:%s,request id:%s, code:%d, data:%s, message:%s" %
        event, request_id, code, str(data), message)


def on_thing_call_service(self, identifier, request_id, params, userdata):
    logging.info("on_thing_call_service identifier:%s, request id:%s, params:%s" % (identifier, request_id, params))
    if identifier == "Operation_Service":
        pass
        # lk.thing_answer_service(identifier, request_id, code, params)


lk.enable_logger(level=logging.DEBUG)
lk.thing_setup("model.json")
lk.on_connect = on_connect
lk.on_disconnect = on_disconnect
lk.on_thing_enable = on_thing_enable
lk.on_subscribe_topic = on_subscribe_topic
lk.on_unsubscribe_topic = on_unsubscribe_topic
lk.on_topic_message = on_topic_message
lk.on_publish_topic = on_publish_topic
lk.on_thing_call_service = on_thing_call_service
lk.on_thing_event_post = on_thing_event_post
lk.on_thing_prop_changed = on_thing_prop_changed
lk.on_thing_prop_post = on_thing_prop_post
lk.on_thing_call_service = on_thing_call_service

# 连接
lk.connect_async()
lk.start_worker_loop()
time.sleep(3)  # 延时

# 属性上报测试
prop_data = {
    "PowerSwitch": 0,
    "Counter": 1
}
rc, request_id = lk.thing_post_property(prop_data)
if rc == 0:
    logging.info("thing_post_property success:%r,mid:%r,\npost_data:%s" % (rc, request_id, prop_data))
else:
    logging.warning("thing_post_property failed:%d" % rc)

# 事件上报测试
events = ("HardwareError", {"ErrorCode": random.randint(0, 3)})
rc1, request_id1 = lk.thing_trigger_event(events)
if rc1 == 0:
    logging.info("thing_trigger_event success:%r,mid:%r,\npost_data:%s" % (rc1, request_id1, events))
else:
    logging.warning("thing_trigger_event failed:%d" % rc)

while True:
    pass
