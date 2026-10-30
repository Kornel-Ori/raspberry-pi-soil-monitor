# Raspberry Pi Soil Moisture Monitoring System

A Raspberry Pi-based project that monitors soil moisture in multiple plants or growing areas using soil moisture sensors and LED indicators. The system helps users identify when plants need watering by providing a simple visual indication of soil conditions.

## Project Overview

The goal of this project is to build a soil moisture monitoring system capable of collecting readings from multiple sensors and displaying the results through LED indicators.

Each sensor monitors the moisture level of the soil in a plant pot or growing area. The Raspberry Pi processes the readings and activates the appropriate LED indicator based on the measured moisture level.

## Objectives

- Monitor soil moisture in multiple plants or growing areas.
- Read and process moisture sensor data using a Raspberry Pi.
- Use LED indicators to communicate soil moisture conditions.
- Identify plants that may need watering.
- Develop a modular system that can be expanded with additional sensors.
- Practise Python programming, GPIO control and hardware integration.

## Hardware Requirements

- Raspberry Pi
- Multiple soil moisture sensors (preferably capacitive sensors)
- MCP3008 analogue-to-digital converter (ADC), if using analogue sensors
- LEDs for moisture status indication
- Current-limiting resistors for the LEDs
- Breadboard and jumper wires
- Power supply for the Raspberry Pi
- Plant pots and soil for testing

**Note:** The Raspberry Pi does not have built-in analogue inputs. If the selected soil moisture sensors provide analogue output, an ADC such as the MCP3008 is required to read their values.

## How It Works

1. Each soil moisture sensor measures the moisture level of a different plant or growing area.
2. The Raspberry Pi reads the sensor values.
3. The software compares each reading against configurable moisture thresholds.
4. The corresponding LED indicates the current moisture status.
5. The process repeats continuously, allowing the system to monitor multiple plants.

### LED Indicator Logic

The following status scheme is a proposed starting point and can be adjusted during testing.

| LED indicator | Soil condition | Suggested action |
|---|---|---|
| Red | Dry soil | Water the plant |
| Yellow | Moisture is getting low | Check the soil |
| Green | Sufficient moisture | No watering needed |

The exact sensor thresholds will depend on the sensor type, soil composition and calibration results.

## Software Requirements

- Python 3
- Raspberry Pi OS
- GPIO control library, such as `gpiozero`
- SPI interface and an appropriate library for the MCP3008, if required

## Project Structure

A possible project structure is:

```text
raspberry-pi-soil-monitor/
├── README.md
├── main.py
├── sensors/
│   └── soil_sensor.py
├── indicators/
│   └── led_indicator.py
├── config.py
├── requirements.txt
├── tests/
│   └── test_soil_sensor.py
└── .gitignore
```

The structure may change as the project develops.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Kornel-Ori/raspberry-pi-soil-monitor.git
cd raspberry-pi-soil-monitor
```

### 2. Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Once the required libraries have been added to `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

### 4. Connect the hardware

Connect the soil moisture sensors, ADC if needed, and LEDs according to the selected hardware and GPIO pin configuration.

**Important:** Check the sensor and ADC voltage requirements before connecting them. Raspberry Pi GPIO pins use 3.3 V logic and are not 5 V tolerant.

### 5. Run the application

After implementing the main program, run:

```bash
python3 main.py
```

## Development Plan

- [ ] Select and test the soil moisture sensors.
- [ ] Connect and configure the ADC, if required.
- [ ] Read moisture values from a single sensor.
- [ ] Integrate multiple soil moisture sensors.
- [ ] Connect and test LED indicators.
- [ ] Implement moisture thresholds and status logic.
- [ ] Calibrate sensors using dry and moist soil.
- [ ] Test the complete system with multiple plants.
- [ ] Document the wiring and configuration.
- [ ] Add error handling and automated tests.

## Future Improvements

Potential future features include:

- A dashboard displaying readings from all sensors.
- Historical moisture data and graphs.
- Notifications when a plant needs watering.
- Wi-Fi-based monitoring from another device.
- Data logging to a file or database.
- Integration with an automatic watering system.

## Safety and Reliability

- Use appropriate current-limiting resistors with LEDs.
- Verify wiring before powering the circuit.
- Keep the Raspberry Pi and exposed electronics away from water and damp soil.
- Calibrate each sensor before setting moisture thresholds.
- Avoid leaving ordinary resistive moisture sensors powered continuously, as they may corrode more quickly.

## License

This project is developed for educational and personal use. A suitable open-source licence can be added as the project progresses.
