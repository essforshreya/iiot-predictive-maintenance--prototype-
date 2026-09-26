# IIoT Predictive Maintenance Prototype ⚙️

An IoT and machine-learning prototype for monitoring machine
operating conditions and identifying abnormal behavior using
temperature, vibration, current, and RPM telemetry.

The current prototype uses simulated machine telemetry to test
the MQTT communication and anomaly-detection pipeline. An ESP32
firmware template is included for future integration with physical
industrial sensors.

## Current Project Status

### Implemented
- MQTT-based telemetry pipeline
- Machine-data simulator
- Python anomaly-detection pipeline
- Isolation Forest model
- Anomaly detection and health-score output
- ESP32 firmware architecture

### Planned
- Physical vibration sensor integration
- Temperature sensor integration
- Current sensing
- RPM measurement
- Real ESP32 telemetry
- Grafana/time-series dashboard
