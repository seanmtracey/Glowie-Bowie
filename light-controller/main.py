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

lastWeatherUpdate = None
loopRainbow = False

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

def wheel(pos):
	# Input a value 0 to 255 to get a color value.
	# The colours are a transition r - g - b - back to r.
	if pos < 0 or pos > 255:
		r = g = b = 0
	elif pos < 85:
		r = int(pos * 3)
		g = int(255 - pos * 3)
		b = 0
	elif pos < 170:
		pos -= 85
		r = int(255 - pos * 3)
		g = 0
		b = int(pos * 3)
	else:
		pos -= 170
		r = 0
		g = int(pos * 3)
		b = int(255 - pos * 3)
	return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):

	global loopRainbow

	for j in range(255):
		for i in range(num_pixels):
			pixel_index = (i * 256 // num_pixels) + j
			pixels[i] = wheel(pixel_index & 255)
		pixels.show()
		time.sleep(wait)

	if loopRainbow == True:
		rainbow_cycle(wait)

def trigger_rainbow_cycle(client, userdata, message):

	global loopRainbow
	
	print("Received a new message from topic: ", message.topic)
	payload = json.loads(message.payload)

	print(payload)
	print(payload['state'] == "on")
	if payload['state'] == "on":
		
		loopRainbow = True
		rainbow_cycle(0.010)

	else :
		loopRainbow = False
		handlePayload(None, None, lastWeatherUpdate)


def handlePayload(client, userdata, message):

	global lastWeatherUpdate
	global loopRainbow

	print("Received a new message from topic: ", message.topic)
	print("\t", json.loads(message.payload))
	print("\n\n")

	info = json.loads(message.payload)
	
	lastWeatherUpdate = message

	print(info)
	leftColorTuple = (info['lightSettings']['leftStrip']['color'][0], info['lightSettings']['leftStrip']['color'][1], info['lightSettings']['leftStrip']['color'][2])
	rightColorTuple = (info['lightSettings']['rightStrip']['color'][0], info['lightSettings']['rightStrip']['color'][1], info['lightSettings']['rightStrip']['color'][2])

	print("Left strip color will be:", leftColorTuple)
	print("Right strip color will be:", rightColorTuple)

	if loopRainbow == False:

		display_lights(0, num_pixels, (0,0,0))

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
myMQTTClient.subscribe("glowie_bowie/lights/rainbow", 1, trigger_rainbow_cycle)

leftColorTuple = (255,0,0)
rightColorTuple = (0,255,0)

display_lights(0, 20, leftColorTuple)
display_lights(43, 61, leftColorTuple)
display_lights(78, 100, rightColorTuple)

pixels.show()

time.sleep(5)

pixels.fill( (0,0,0,0) )
pixels.show()

while True:
	time.sleep(1)