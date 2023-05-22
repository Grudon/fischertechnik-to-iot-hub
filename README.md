# fischertechnik-to-iot-hub
Connecting a Fischertechnik Training Factory Industry 4.0 to Azure IoT Hub via a Raspberry Pi.

Please set up your parameters (subscribed topics, IP address of WiFi router, IoT Hub Connection String) first in parameters.py. Documentation regarding the MQTT-interface of the Training Factory can be found here: https://github.com/fischertechnik/txt_training_factory/blob/master/TxtSmartFactoryLib/doc/MqttInterface.md

Supports the method "order" with the key "colour" and the values "RED", "BLUE" or "WHITE".

Place the downloaded repository folder in /home/user/Documents. Edit the file path in the startup script if necessary.
