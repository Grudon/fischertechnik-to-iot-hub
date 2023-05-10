#Raspberry to Azure IoT Hub

import asyncio
import os
from azure.iot.device.aio import IoTHubDeviceClient

CONNECTION_STRING = "HostName=IoT-Hub-Tobias1.azure-devices.net;DeviceId=raspberry_bridge;SharedAccessKey=DedCWlDQKFwHFtChf3feKSaA7xsZ7TEpondoHaWQbaY="
TOTAL_MESSAGES_SENT = 0


async def main():
    # Fetch the connection string from an environment variable
    conn_str = CONNECTION_STRING

    # Create instance of the device client using the connection string
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client.
    await device_client.connect()
		
    # Send a single message
    print("Sending message...")
    await device_client.send_message("This is a message that is being sent")
    print("Message successfully sent!")

    # Finally, shut down the client
    await device_client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
