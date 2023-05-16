#!/bin/sh

#Check for connecion to Wifi (has received an IP-address?)
while [ "$(hostname -I)" = "" ]; do
	echo -e "\e[1A\e[KNo Wifi connection: $(date)"
	sleep 1
done

echo "\n$(date): Connected to WiFi\n"

#Ping a server to check if connected to internet (Google DNS)
serverAdr="8.8.8.8"

ping -c 1 $serverAdr > /dev/null 2>&1
while [ $? -ne 0 ]; do
	echo -e "\e[1A\e[K $(date): Pinging ${serverAdr} ..."
	sleep 1
	ping -c 1 $serverAdr > /dev/null 2>&1
done

echo "$(date): Connected to internet\n";

python3 /home/user/Documents/fischertechnik-to-iot-hub-main/main-client.py
