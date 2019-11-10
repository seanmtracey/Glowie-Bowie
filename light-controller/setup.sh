#! /bin/bash

virtualenv -p python3 ./venv
source ./venv/bin/activate
pip install paho-mqtt RPI.GPIO rpi_ws281x adafruit-blinka adafruit-circuitpython-neopixel