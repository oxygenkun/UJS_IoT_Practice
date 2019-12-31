import json
import logging
import random
import time

from linkkit import linkkit


class CloudDaemon(object):
    # 属性
    __properties = {
        'power': 0,
        'counter': 0
    }
    __power = 0
    __counter = 0

    def __init__(self, config_path, model_path):
        LOG_FORMAT = "%(thread)d %(asctime)s  %(levelname)s %(filename)s %(lineno)d %(message)s"
        DATE_FORMAT = "%m/%d/%Y-%H:%M:%S-%p"
        logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT)
        # 读取相关配置：HostName 、ProductKey 、DeviceName 、DeviceSecret
        with open(config_path, 'r') as f:
            conf = json.load(f)
        self.lk = linkkit.LinkKit(
            host_name=conf['HostName'],
            product_key=conf['ProductKey'],
            device_name=conf['DeviceName'],
            device_secret=conf['DeviceSecret']  # 一机一密
        )

        self.lk.enable_logger(level=logging.DEBUG)
        self.lk.thing_setup("model.json")
        self.lk.on_connect = self.on_connect
        self.lk.on_disconnect = self.on_disconnect
        self.lk.on_thing_enable = self.on_thing_enable
        self.lk.on_subscribe_topic = self.on_subscribe_topic
        self.lk.on_unsubscribe_topic = self.on_unsubscribe_topic
        self.lk.on_topic_message = self.on_topic_message
        self.lk.on_publish_topic = self.on_publish_topic
        self.lk.on_thing_call_service = self.on_thing_call_service
        self.lk.on_thing_event_post = self.on_thing_event_post
        self.lk.on_thing_prop_changed = self.on_thing_prop_changed
        self.lk.on_thing_prop_post = self.on_thing_prop_post

    # 连接
    def connect_cloud(self):
        self.lk.connect_async()
        self.lk.start_worker_loop()

    def set_power(self, val):
        if val is True or val is False:
            self.power = val

    ######################################
    # 模版模式，观察者模式
    #####################################
    # 连接
    def on_connect(self, session_flag, rc, userdata):
        logging.info("on_connect:%d,rc:%d,userdata:" % (session_flag, rc))

    # 断开连接
    def on_disconnect(self, rc, userdata):
        logging.info("on_disconnect:rc:%d,userdata:" % rc)

    # 订阅
    def on_subscribe_topic(self, mid, granted_qos, userdata):
        logging.info("on_subscribe_topic mid:%d, granted_qos:%s" %
                     (mid, str(','.join('%s' % it for it in granted_qos))))

    # 取消订阅
    def on_unsubscribe_topic(self, mid, userdata):
        logging.info("on_unsubscribe_topic mid:%d" % mid)

    # Topic消息
    def on_topic_message(self, topic, payload, qos, userdata):
        logging.info("on_topic_message:" + topic + " payload:" + str(payload) + " qos:" + str(qos))

    # 发布消息
    def on_publish_topic(self, mid, userdata):
        logging.info("on_publish_topic mid:%d" % mid)

    # 上报属性
    def on_thing_prop_post(self, request_id, code, data, message, userdata):
        logging.info("on_thing_prop_post request id:%s, code:%d message:%s, data:%s,userdata:%s" %
                     (request_id, code, message, data, userdata))

    # 用户可以进行属性上报，事件上报，服务响应，此调用需要在连接前
    def on_thing_enable(self, userdata):
        logging.info("on_thing_enable")

    def on_thing_disable(self, userdata):
        print("on_thing_disable")

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

    # 云端设置本地端属性
    def on_thing_prop_changed(self, message, userdata):

        # 属性上报测试
        prop_data = {
            "PowerSwitch": 0,
            "Counter": 1
        }
        if "PowerSwitch" in message.keys():
            self.prop_data["PowerSwitch"] = message["PowerSwitch"]
        elif "WindSpeed" in message.keys():
            self.prop_data["WindSpeed"] = message["WindSpeed"]
        elif "WorkMode" in message.keys():
            self.prop_data["WorkMode"] = message["WorkMode"]
        else:
            logging.warning("wrong data:%s" % message)
        self.lk.thing_post_property(message)  # SDK不会主动上报属性变化，如需要修改后再次上报云端，需要调用thing_post_property()发送
        print('prop_data:', self.prop_data)
        print('message:', message)
        logging.info("on_thing_prop_changed  data:%s " % message)

    def test(self):
        # 属性上报测试
        prop_data = {
            "PowerSwitch": self.__power,
            "Counter": self.__counter
        }
        rc, request_id = self.lk.thing_post_property(prop_data)
        if rc == 0:
            logging.info("thing_post_property success:%r,mid:%r,\npost_data:%s" % (rc, request_id, prop_data))
        else:
            logging.warning("thing_post_property failed:%d" % rc)

        # 事件上报测试
        events = ("HardwareError", {"ErrorCode": random.randint(0, 3)})
        rc1, request_id1 = self.lk.thing_trigger_event(events)
        if rc1 == 0:
            logging.info("thing_trigger_event success:%r,mid:%r,\npost_data:%s" % (rc1, request_id1, events))
        else:
            logging.warning("thing_trigger_event failed:%d" % rc)

        while True:
            pass
