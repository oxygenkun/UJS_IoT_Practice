import time
import unittest

from raspberryPi.main import Process
import raspberryPi.ArduinoDaemon as arduino
import raspberryPi.CloudDaemon as cloud


class TestProcess(unittest.TestCase):


    def test_set_power(self):
        usb = arduino.USBInterface()
        myProcess = Process(usb)
       # aliyun = cloud.CloudDaemon(config_path="config.json", model_path="model.json",process = myProcess)
        #aliyun.connect_cloud()
        time.sleep(5)
        self.assertEqual(myProcess.set_power(1),True)
        self.assertEqual(myProcess.set_power(0),False)

    def test_get_temp(self):
        usb = arduino.USBInterface()
        myProcess = Process(usb)
       # aliyun = cloud.CloudDaemon(config_path="config.json", model_path="model.json",process = myProcess)
        #aliyun.connect_cloud()
        time.sleep(5)
        data = myProcess.get_temp()
        print(data)
