import paho.mqtt.client as mqtt
import board
import neopixel
import json

pixels = neopixel.NeoPixel(board.D16, 36, brightness=0.5, auto_write = False, pixel_order = neopixel.RGBW)

def display_lights(matrix):

    if matrix is None:
        
        print("No matrix of light values has been passed to display")
        return False
    
    if len(matrix) is 0:
        pixels.fill( (0,0,0,0) )

    for idx in range(0, 18):
        pixels[idx] = matrix[idx]

    pixels.show()

def set_brightness(level):
    pixels.brightness(level)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("glowie-bowie/lights")
    client.subscribe("glowie-bowie/brightness")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    if msg.topic == "glowie-bowie/lights":
        display_lights(msg.payload)

    if msg.topic == "glowie-bowie/brightness":
        print("Set Brightness Levels")
        set_brightness( float(msg.payload) )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipse.org", 1883, 60)
client.loop_forever()