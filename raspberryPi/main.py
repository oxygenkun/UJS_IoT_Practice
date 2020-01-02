import json
import time
import raspberryPi.ArduinoDaemon as arduino
import raspberryPi.CloudDaemon as cloud


def main():
    usb = arduino.USBInterface()
    aliyun = cloud.CloudDaemon(config_path="config.json", model_path="model.json")
    aliyun.connect_cloud()
    myProcess = Process(usb, aliyun)

    while 1:
        time.sleep(60)
        myProcess.get_temp()
        aliyun.upload_temperature_and_humidity()


class Process(object):
    cmd = ["ps", "dht"]

    def __init__(self, usb, aliyun):
        if isinstance(usb, arduino.USBInterface):
            self.__arduino = usb
        if isinstance(aliyun, cloud.CloudDaemon):
            self.__aliyun = aliyun

    def power_set(self):
        pass

    def get_temp(self):
        cmd = {"cmd": "dht"}
        self.__arduino.put_info(json.dumps(cmd).encode('utf-8'))
        result = json.loads(self.__arduino.get_info())
        if result["cmd"] == "dht":
            data = result["data"]
            self.__aliyun.set_humidity(data["humi"])
            self.__aliyun.set_temperature(data["temp"])


if __name__ == '__main__':
    main()
