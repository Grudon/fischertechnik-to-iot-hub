#!/bin/sh
# Startup script to check if device has an internet connection before client script starts
# Check if connected to Wifi (has device received an IP-address?)
while [ "$(hostname -I)" = "" ]; do
	echo -e "\e[1A\e[KNo Wifi connection: $(date)"
	sleep 1
done

echo "\n$(date): Connected to WiFi\n"

# Ping a webserver to check if device is connected to internet (Google DNS)
serverAdr="8.8.8.8"

ping -c 1 $serverAdr > /dev/null 2>&1
while [ $? -ne 0 ]; do
	echo -e "\e[1A\e[K $(date): Pinging ${serverAdr} ..."
	sleep 1
	ping -c 1 $serverAdr > /dev/null 2>&1
done

echo "$(date): Connected to internet\n";

# Start script in a new terminal window if all tests succeeded

python3 /home/user/Documents/fischertechnik-to-iot-hub-main/main-client.py
