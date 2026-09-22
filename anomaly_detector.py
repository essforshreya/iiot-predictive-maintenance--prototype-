import json
import os
from collections import deque

import numpy as np
import paho.mqtt.client as mqtt
from sklearn.ensemble import IsolationForest

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "factory/machine01/telemetry")

FEATURES = ["temperature", "vibration", "current", "rpm"]
BASELINE_SIZE = 40
history = deque(maxlen=BASELINE_SIZE)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT:", reason_code)
    client.subscribe(TOPIC)
    print("Subscribed to:", TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        vector = [float(payload[name]) for name in FEATURES]
        history.append(vector)

        print("Telemetry:", payload)

        if len(history) < BASELINE_SIZE:
            print(f"Building baseline: {len(history)}/{BASELINE_SIZE}\n")
            return

        X = np.array(history)

        model = IsolationForest(
            n_estimators=150,
            contamination=0.08,
            random_state=42
        )
        model.fit(X)

        current = np.array(vector).reshape(1, -1)
        prediction = model.predict(current)[0]
        score = float(model.decision_function(current)[0])
        anomaly = prediction == -1

        if anomaly:
            health = max(0, min(59, int(50 + score * 10)))
        else:
            health = max(60, min(100, int(80 + score * 20)))

        print("Anomaly:", anomaly)
        print("Anomaly score:", round(score, 4))
        print(f"Health score: {health}/100")

        if anomaly:
            print("WARNING: Possible abnormal machine condition detected.")

        print()

    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        print("Invalid telemetry:", exc)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
print(f"Listening on {BROKER}:{PORT}")
client.loop_forever()
