from dotenv import load_dotenv
import board, neopixel, json, os, time

load_dotenv(verbose = True)

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

MQTT_TOPIC = os.getenv("MQTT_TOPIC")

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient(os.getenv("CLIENT_ID"))
# For TLS mutual authentication
myMQTTClient.configureEndpoint(os.getenv("MQTT_HOST"), 8883)

pixel_pin = board.D18
num_pixels = 120
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER
)


def display_lights(start_pixel = 0, end_pixel = 0, color = (255, 255, 255)):

    for idx in range(start_pixel, end_pixel):
        pixels[idx] = color

    pixels.show()

def set_brightness(level):
    pixels.brightness(level)

'''
Example payload

{'lightSettings': {'leftStrip': {'color': [150, 255, 255]}, 'rightStrip': {'color': [190, 255, 200]}}, 'time': 1643085608, 'weatherType': 'clouds'}

'''

def handlePayload(client, userdata, message):
	print("Received a new message from topic: ", message.topic)
	print("\t", json.loads(message.payload))
	print("\n\n")

	info = json.loads(message.payload)
	print(info)
	leftColorTuple = (info['lightSettings']['leftStrip']['color'][0], info['lightSettings']['leftStrip']['color'][1], info['lightSettings']['leftStrip']['color'][2])
	rightColorTuple = (info['lightSettings']['rightStrip']['color'][0], info['lightSettings']['rightStrip']['color'][1], info['lightSettings']['rightStrip']['color'][2])

	print("Left strip color will be:", leftColorTuple)
	print("Right strip color will be:", rightColorTuple)

	display_lights(0, 20, leftColorTuple)
	display_lights(43, 61, leftColorTuple)
	display_lights(78, 97, rightColorTuple)


CA_PATH = os.path.join(os.path.dirname(__file__), os.getenv("CA_PATH"))
PRIVATE_KEY_PATH = os.path.join(os.path.dirname(__file__), os.getenv("PRIVATE_KEY_PATH"))
CERTIFICATE_PATH = os.path.join(os.path.dirname(__file__), os.getenv("CERTIFICATE_PATH"))
print(CA_PATH)

myMQTTClient.configureCredentials(CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5) 

print("Connecting to AWS IoT Broker")
myMQTTClient.connect()
print("Subscribing to topic:", MQTT_TOPIC)
myMQTTClient.subscribe(MQTT_TOPIC, 1, handlePayload)

leftColorTuple = (255,0,0)
rightColorTuple = (0,255,0)

display_lights(0, 20, leftColorTuple)
display_lights(43, 61, leftColorTuple)
display_lights(78, 100, rightColorTuple)

pixels.show()

time.sleep(5)

# exit()

pixels.fill( (0,0,0,0) )
pixels.show()

while True:
	time.sleep(1)