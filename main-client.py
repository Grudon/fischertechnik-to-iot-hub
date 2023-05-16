#Please configure parameters.py first

import asyncio
import os
from azure.iot.device import IoTHubDeviceClient, MethodResponse, Message
import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json
from parameter import data

def toJSON(a):
    return json.dumps(a)

def toObject(b):
    return json.loads(b)

def create_iot_client():
    client = IoTHubDeviceClient.create_from_connection_string(data["CONNECTION_STRING"])

    # define behavior for receiving a message
    def iot_message_handler(message):
        print("IOT message received:")
        print(message.data)

    # define behavior for receiving direct methods
    def method_handler(method_request):
        print("Received Method:", method_request.name, "payload:", method_request.payload)
        if method_request.name == "order":
            result = mqtt_publish(method_request.payload)
            payload = {"result": result}
            status = 200
            print("Completed method 'order'")
        else:
            payload = {}
            status = 400
            print("Unknown direct method request")
        method_response = MethodResponse.create_from_method_request(method_request, status, payload)
        client.send_method_response(method_response)

    # set the incoming data handlers on the client
    client.on_message_received = iot_message_handler
    client.on_method_request_received = method_handler

    return client

#Send published MQTT Mssages to IoT Hub
def send_telemetry(client, msg):
        print("Sending Telemetry...")
        try:
            client.send_message(toJSON(msg))
            print("Telemetry sent!\n")
        except Exception as e:
            print("Error:", str(e))
            print("Sending telemetry failed")

def create_mqtt_client():
    client = mqtt.Client("raspberry-client")

    def mqtt_message_handler(client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8","ignore"))
        print("MQTT Publish Received, Topic:", topic, "and Message:\n", m_decode)
        iot_message = {
            "topic":topic,
            "payload": toObject(m_decode)
        }
        send_telemetry(iot_client, iot_message)
        return True
    
    client.on_message = mqtt_message_handler

    return client

# return ISO 8601 datetime-stamp 10 seconds in the future
def current_datetime():
    ts = time.time() + 10
    dt = datetime.utcfromtimestamp(ts)
    iso = dt.isoformat("T","milliseconds")
    iso += "Z"
    return iso

# publish the production order
# colour must be sent via Attribute "colour"
# can be "RED", "BLUE" or "WHITE"
def mqtt_publish(payload):
    datetime = current_datetime()
    print(payload["colour"])
    data_json={
        "ts":datetime,
        "type":payload["colour"]
    }
    mqtt_json = toJSON(data_json)
    print("Publishing to", data["PUB_TOPIC"], ":\n", mqtt_json)
    mqtt_client.publish(data["PUB_TOPIC"], mqtt_json)

# Main Function
# Create clients and connect them
# Subscribe to all topics
# Run in Loop except when Errors or UserInput happen    
async def main():
    global iot_client
    global mqtt_client

    iot_client = create_iot_client()
    mqtt_client = create_mqtt_client()

    print("Connecting to IoT Hub...")
    iot_client.connect()
    print("Iot Hub Connection Success!")

    print("Connecting to MQTT Broker...")
    mqtt_client.connect(data["BROKER"])
    print("MQTT Connection Success!")

    for t in data["SUB_TOPICS"]:
        mqtt_client.subscribe(t)

    mqtt_client.loop_start()

    while True:
        try:
            await asyncio.sleep(5)
            print("running...")
        except KeyboardInterrupt:
            print("User exit!")
            break
        except Exception:
            print("Unexpected error")
            break
   
   #Shut down for graceful exit
    iot_client.shutdown()
    mqtt_client.disconnect()
    print("Disconnected all clients.")
        

#run main()
if __name__ == "__main__":
    asyncio.run(main())
