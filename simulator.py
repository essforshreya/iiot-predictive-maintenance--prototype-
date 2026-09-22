import json
import os
import random
import time
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "factory/machine01/telemetry")

def make_reading(anomaly=False):
    if anomaly:
        return {
            "device_id": "machine-01",
            "temperature": round(random.gauss(78, 4), 2),
            "vibration": round(random.gauss(4.8, 0.6), 2),
            "current": round(random.gauss(5.2, 0.5), 2),
            "rpm": round(random.gauss(1180, 70), 2),
        }

    return {
        "device_id": "machine-01",
        "temperature": round(random.gauss(42, 2), 2),
        "vibration": round(max(0.1, random.gauss(1.5, 0.2)), 2),
        "current": round(max(0.2, random.gauss(2.5, 0.25)), 2),
        "rpm": round(random.gauss(1500, 35), 2),
    }

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT, 60)
client.loop_start()

print(f"Publishing to {BROKER}:{PORT}/{TOPIC}")
counter = 0

try:
    while True:
        anomaly = counter % 12 == 0
        payload = json.dumps(make_reading(anomaly))
        client.publish(TOPIC, payload)
        print(payload)
        counter += 1
        time.sleep(3)
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
