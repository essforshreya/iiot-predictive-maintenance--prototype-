# ESP32 IoT Predictive Maintenance Prototype ⚙️

An IoT-based predictive-maintenance prototype for monitoring machine health using temperature, vibration, current, and RPM data.

> **Status:** Software prototype / starter implementation. The Python pipeline is testable with simulated machine data. The ESP32 firmware is a hardware template; real predictive-maintenance hardware has not yet been claimed as completed.

## Architecture

Machine sensors → ESP32 → MQTT broker → Python anomaly detector → health score / anomaly flag

## Repository

```text
esp32-predictive-maintenance/
├── README.md
├── .gitignore
├── esp32_node/
│   ├── maintenance_node.ino
│   ├── config.h
│   └── secrets.example.h
├── python/
│   ├── simulator.py
│   ├── anomaly_detector.py
│   └── requirements.txt
└── data/
    └── .gitkeep
```

## Intended measurements

| Parameter | Purpose |
|---|---|
| Temperature | Detect overheating |
| Vibration | Detect abnormal mechanical vibration |
| Current | Detect unusual electrical load |
| RPM | Detect speed changes |

The exact physical sensors and GPIO mapping should be finalized after hardware selection.

## MQTT payload

```json
{
  "device_id": "machine-01",
  "temperature": 42.5,
  "vibration": 1.82,
  "current": 2.4,
  "rpm": 1480
}
```

## Run the software prototype

Install dependencies:

```bash
pip install -r python/requirements.txt
```

Run an MQTT broker locally, then in one terminal:

```bash
python python/anomaly_detector.py
```

In another terminal:

```bash
python python/simulator.py
```

The simulator generates normal readings and occasional abnormal readings, allowing the anomaly-detection pipeline to be tested before connecting an ESP32.

## ESP32 firmware

`esp32_node/maintenance_node.ino` is a starter hardware template. Its sensor-reading functions contain placeholders because the exact sensors and calibration have not been finalized.

Create a local `secrets.h` from `secrets.example.h` and add Wi-Fi/MQTT credentials. Do not commit real credentials.

## Detection

The Python pipeline uses Isolation Forest to identify observations that differ from the learned operating baseline. It reports an anomaly flag, anomaly score, and a simple prototype health score.

The health score is for demonstration and is **not** an industrial safety rating or guaranteed failure prediction.

## Future improvements

- Connect real vibration, temperature, current and RPM sensors
- Calibrate sensor ranges
- Store historical telemetry in a time-series database
- Build a Grafana dashboard
- Add machine-specific baselines
- Add alerts
- Evaluate additional anomaly-detection methods
- Add remaining-useful-life prediction after obtaining labelled failure data

## Author

**Shreya Roy**  
B.Tech — Internet of Things (IIOT), GGSIPU
