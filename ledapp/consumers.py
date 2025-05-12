import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import Adafruit_DHT
import RPi.GPIO as GPIO

LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

class DHTConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = True
        asyncio.create_task(self.send_sensor_data())

    async def disconnect(self, close_code):
        self.running = False

    async def receive(self, text_data):
        data = json.loads(text_data)

        if 'command' in data:
            if data['command'] == 'on':
                GPIO.output(LED_PIN, True)
            elif data['command'] == 'off':
                GPIO.output(LED_PIN, False)
            elif data['command'] == 'toggle':
                GPIO.output(LED_PIN, not GPIO.input(LED_PIN))

            await self.send(text_data=json.dumps({
                'led': GPIO.input(LED_PIN)
            }))

    async def send_sensor_data(self):
        while self.running:
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
                await self.send(text_data=json.dumps({
                    'temperature': round(temperature, 1),
                    'humidity': round(humidity, 1),
                    'led': GPIO.input(LED_PIN)
                }))
            await asyncio.sleep(5)
