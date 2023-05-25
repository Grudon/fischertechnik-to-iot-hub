# Parameters - change to preferences
# Please replace the connection string

data = {
    # Device's Primary Connection String from IoT Hub
    "CONNECTION_STRING" : "YOUR_PRIMARY_CONNECTION_STRING",
    # IP address of the MQTT broker on Fischertechnik (Main TXT-0)
    "BROKER" : "192.168.0.10",
    # Topics to subscribe to, any amount possible
    "SUB_TOPICS" : ["f/i/order",
        "f/i/stock", 
        "f/i/state/hbw", 
        "f/i/state/mpo",
        "f/i/state/vgr", 
        "f/i/state/sld", 
        "f/i/state/dsi", 
        "f/i/state/dso"],
    # Topic to publish to, can only be 1
    "PUB_TOPIC" : "f/o/order",
}
