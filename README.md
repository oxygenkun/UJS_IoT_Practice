# UJS_IoT_Practice

使用 arduino+raspberry+aliyun IoT 搭建智能项目的实践课程练习

# 环境配置

##  树莓派 python 环境配置

1. 创建和激活 VirtualEnvironments（可跳过）

2. 使用pip自动安装linkkit

```shell script
pip install aliyun-iot-linkkit
```

3. 使用pip自动安装Advanced Python Scheduler（APScheduler）

```shell script
pip install apscheduler
```
   
## arduino 设备配置

1. arduino需要准备：
    
    1. Arduino Uno
    2. DHT11 温湿度传感器
    3. 130 DC Motor 电机
    4. LED灯

2. led灯、温湿度传感器、电机通过宏定义确定pin脚位置，需要根据实际情况修改```arduino/test/test.ino```。

    ```c
    #define LEDPIN  2
    #define DHTPIN 4
    #define DHTTYPE DHT11
    #define MTOTRPIN 6
    ```

3. 将 ```arduino/test/test.ino```烧录进arduino uno。

## 树莓派与arduino连接

1. 根据串口地址，修改```raspberryPi/ArduinoDaemon.py```中串口地址。
    
## 阿里云设备上线

1. 先设定产品、设备信息，获得三要素（ProductKey、DeviceName、DeviceSecret）

2. 在“产品”->“功能定义”->“自定义功能”内，设置产品物模型。
   
    本次设定有：
   
    - 电源开关
    - 温度
    - 湿度
    - 风扇
    
3. 根据设定修改```raspberryPi/CloudDaenom.py```中CloudDaemon类成员相应物模型标识符：
    
    ```python
    class CloudDaemon(object):
        __power_name = 'PowerSwitch'
        __temperature_name = 'Temp'
        __humidity_name = 'Humi'
        __fan_name = 'Fan'
    ```

3. 在```raspberryPi/config.json```文件中将设备信息填写
4. 在“产品”->“功能定义”->“自定义功能”中“查看物模型”，并点击导出完整物模型json文件，覆盖```raspberryPi/model.json```

# 运行

在raspberryPi文件夹运行:

```shell script
python3 main.py
```
