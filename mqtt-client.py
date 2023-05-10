import paho.mqtt.client as mqtt
import time
import json

brokers={"broker1":"192.168.0.10"}
#data_json={
#    "ts":"2023-05-05T12:06:40.411Z",
#    "cmd":"read"
#    }

data_json={
    "ts":"2023-05-09T09:44:10.368Z",
    "type":"RED"
}

data_out=json.dumps(data_json)# encode oject to JSON

print ("data out =",data_out)

data_in=data_out
print ("data in =",data_in)

json_in=json.loads(data_in) #convert incoming JSON to object
#print("\n\nJson data command is =",json_in["cmd"])

cont=input("*Enter to Continue*")

###########

def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("Data Received:",m_decode)
    
    m_in=json.loads(m_decode)
    print("Data Received stock #2:",(m_in["stockItems"][1]))

#topic_pub="f/o/nfc/ds"
topic_pub="f/o/order"
topic_sub="f/i/stock"
client=mqtt.Client("pythontest1")
client.on_message=on_message

print("Connecting to broker",brokers["broker1"])
client.connect(brokers["broker1"])

print("Sending data...")
client.publish(topic_pub,data_out)
print("Data sent!")

while True:
    client.loop_start()
    client.subscribe(topic_sub)
    client.loop_stop()

client.disconnect()