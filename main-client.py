#Please configure parameters.py first

import asyncio
import os
from azure.iot.device import IoTHubDeviceClient, MethodResponse, Message
import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json
from parameter import data

# Turn object to JSON
def toJSON(a):
    return json.dumps(a)

# Turn JSON to Object
def toObject(b):
    return json.loads(b)

# Create an instance of the Azure IoT Device client
def create_iot_client():
    client = IoTHubDeviceClient.create_from_connection_string(data["CONNECTION_STRING"])

    # Define behaviour for receiving a message
    def iot_message_handler(message):
        print("IOT message received:")
        print(message.data)

    # Define behaviour for receiving direct methods
    def method_handler(method_request):
        print("Received Method:", method_request.name, "payload:", method_request.payload)
        # How to handle the order-method
        if method_request.name == "order":
            result = mqtt_publish(method_request.payload)
            payload = {"result": result}
            status = 200
            print("Completed method 'order'")
        # If method is not known
        else:
            payload = {}
            status = 400
            print("Unknown direct method request")
        method_response = MethodResponse.create_from_method_request(method_request, status, payload)
        client.send_method_response(method_response)

    # Set the incoming data handlers on the client
    client.on_message_received = iot_message_handler
    client.on_method_request_received = method_handler

    return client

# Send received MQTT Messages to IoT Hub
def send_telemetry(client, msg):
        print("Sending Telemetry...")
        try:
            client.send_message(toJSON(msg))
            print("Telemetry sent!\n")
        except Exception as e:
            print("Error:", str(e))
            print("Sending telemetry failed\n")

# Create an instance of the Paho MQTT client
def create_mqtt_client():
    client = mqtt.Client("raspberry-client")

    # Define behaviour for receiving messages
    def mqtt_message_handler(client, userdata, msg):
        topic = msg.topic
        # Decode payload to an usable format
        m_decode = str(msg.payload.decode("utf-8","ignore"))
        print("MQTT Publish Received, Topic:", topic, "and Message:\n", m_decode)
        iot_message = {
            "topic":topic,
            "payload": toObject(m_decode)
        }
        # Relay received MQTT message to IoT Hub
        send_telemetry(iot_client, iot_message)
        return True
    
    # Set the incoming data handler on the client
    client.on_message = mqtt_message_handler

    return client

# Return Fischertechnik-conform ISO 8601 datetime-stamp 10 seconds in the future
def current_datetime():
    ts = time.time() + 10
    dt = datetime.utcfromtimestamp(ts)
    iso = dt.isoformat("T","milliseconds")
    iso += "Z"
    return iso

# Send the production order via MQTT publish to Fischertechnik
# Colour must be sent via attribute "colour" in IoT Hub payload
# Can be "RED", "BLUE" or "WHITE"
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
    # Global clients because they need to be called in other functons
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

    # Subscribe to all topics in list
    for t in data["SUB_TOPICS"]:
        mqtt_client.subscribe(t)

    # Start network loop for MQTT client to receive messages
    mqtt_client.loop_start()

    # Run forever except when CTRL+C or error
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
        

# Run main()
if __name__ == "__main__":
    asyncio.run(main())
