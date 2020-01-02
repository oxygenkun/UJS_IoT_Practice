import json
import time
import raspberryPi.ArduinoDaemon as arduino
import raspberryPi.CloudDaemon as cloud


def main():
    usb = arduino.USBInterface()
    myProcess = Process(usb)
    aliyun = cloud.CloudDaemon(config_path="config.json", model_path="model.json", process=myProcess)
    aliyun.connect_cloud()

    while 1:
        time.sleep(5)
        aliyun.update_temperature_and_humidity()
        aliyun.upload_temperature_and_humidity()


class Process(object):
    __cmd_power_set = "ps"
    __cmd_dht = "dht"

    def __init__(self, usb):
        if isinstance(usb, arduino.USBInterface):
            self.__arduino = usb

    def set_power(self, val):
        cmd = {
            "cmd": self.__cmd_power_set,
            "par": val
        }
        self.__arduino.put_info(json.dumps(cmd).encode('utf-8'))
        result = json.loads(self.__arduino.get_info())
        if result["cmd"] == "dht" and result["code"] == 200:
            return result["data"]

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


if __name__ == '__main__':
    main()
