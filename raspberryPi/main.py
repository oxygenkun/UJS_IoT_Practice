import json
import time
from apscheduler.schedulers.background import BackgroundScheduler

import raspberryPi.ArduinoDaemon as arduino
import raspberryPi.CloudDaemon as cloud


def main():
    usb = arduino.USBInterface()
    myProcess = Process(usb)
    aliyun = cloud.CloudDaemon(config_path="config.json", model_path="model.json", process=myProcess)
    aliyun.connect_cloud()

    def temperature_and_humidity():
        aliyun.update_temperature_and_humidity()
        aliyun.upload_temperature_and_humidity()

    scheduler = BackgroundScheduler()
    scheduler.add_job(temperature_and_humidity, 'interval', seconds=30)
    try:
        scheduler.start()
    except SystemExit:
        scheduler.shutdown()

    try:
        while True:
            time.sleep(2)
    except SystemExit:
        scheduler.shutdown()


class Process(object):
    __cmd_power_set = "ps"
    __cmd_dht = "dht"
    __cmd_fan_set = 'mot'

    def __init__(self, usb):
        if isinstance(usb, arduino.USBInterface):
            self.__arduino = usb

    def set_power(self, val):
        return self.set_cmd(cmd=self.__cmd_power_set, val=val)

    def get_temp(self):
        cmd = {"cmd": self.__cmd_dht}
        self.__arduino.put_info(json.dumps(cmd).encode('utf-8'))
        try:
            result = json.loads(self.__arduino.get_info())
            if result["cmd"] == "dht":
                data = result["data"]
                return True, data
        except Exception as e:
            return False, {}

    def set_fan(self, val):
        return self.set_cmd(cmd=self.__cmd_fan_set, val=val)

    def set_cmd(self, cmd, val):
        cmd = {"cmd": cmd, "par": val}
        self.__arduino.put_info(json.dumps(cmd).encode('utf-8'))
        result = json.loads(self.__arduino.get_info())
        if result["cmd"] == cmd:
            return True, result["data"]
        else:
            return False, {}


if __name__ == '__main__':
    main()
