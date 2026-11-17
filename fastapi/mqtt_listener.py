import os
import paho.mqtt.client as mqtt

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))


def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe("soilmonitor/#")
    print(f"Connected to MQTT broker. Result: {reason_code}")


client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()