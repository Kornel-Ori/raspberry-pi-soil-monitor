import json
import os
from platform import node
import paho.mqtt.client as mqtt

from database import SessionLocal
import models

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))


def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe("soilmonitor/#")
    print(f"Connected to MQTT broker. Result: {reason_code}")




def on_message(client, userdata, msg):
    try:
        # Convert the MQTT message into a Python dictionary
        payload = json.loads(msg.payload.decode())

        # Extract the Node ID from the topic
        topic_parts = msg.topic.split("/")
        node_id = int(topic_parts[1])

        # Extract the moisture percentage
        moisture_percent = payload["moisture_percent"]

        # Validate moisture value
        if not isinstance(moisture_percent, (int, float)) or isinstance(moisture_percent, bool):
            print("Invalid moisture value: must be a number")
            return

        if not 0 <= moisture_percent <= 100:
            print("Invalid moisture value: must be between 0 and 100")
            return

        print(f"Node ID: {node_id}")
        print(f"Moisture: {moisture_percent}%")

        # Open database session
        db = SessionLocal()

        # Check whether the node exists
        node = db.get(models.Node, node_id)

        if node is None:
            print(f"Invalid Node ID: {node_id}. Node does not exist.")
            db.close()
            return

        try:
            new_reading = models.Reading(
                moisture_percent=moisture_percent,
                node_id=node_id
            )

            db.add(new_reading)
            db.commit()

            print("Reading saved successfully!")

        except Exception as error:
            db.rollback()
            print(f"Database error: {error}")

        finally:
            db.close()

    except (ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"Invalid MQTT message: {error}")



client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect

client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()