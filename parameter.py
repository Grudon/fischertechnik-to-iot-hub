#Parameters
#Please add your device's Primary Connection String from IoT Hub

data = {
    "CONNECTION_STRING" : "YOUR_PRIMARY_CONNECTION_STRING",
    "BROKER" : "192.168.0.10",
    "SUB_TOPICS" : ["f/i/order",
        "f/i/stock", "f/i/state/hbw", 
        "f/i/state/mpo", "f/i/state/vgr", 
        "f/i/state/sld", 
        "f/i/state/dsi", 
        "f/i/state/dso"],
    "PUB_TOPIC" : "f/o/order",
}
