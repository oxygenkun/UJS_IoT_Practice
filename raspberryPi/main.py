import json

import raspberryPi.ArduinoDaemon as arduino
import raspberryPi.CloudDaemon as cloud

def main():
    usb = arduino.USBInterface()
    aliyun = cloud.CloudDaemon()
    test_json = {"cmd": "ps",
                 "par": 1
                 }
    usb.put_info((json.dumps(test_json)+"\n").encode('utf-8'))
    while 1:
        usb.get_info()


if __name__ == '__main__':
    main()
