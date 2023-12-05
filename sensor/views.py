from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import Adafruit_DHT
import time
from gpiozero import LED

# Create your views here.

led_r = LED(23)
led_g = LED(24)
led_b = LED(25)
sensor = Adafruit_DHT.DHT22
sensor_pin = 4

def merenje():
	# ocitaj temperaturu i vlaznost
	vlaznost, temperatura = Adafruit_DHT.read_retry(sensor, sensor_pin)

	global kalVlaznost
	global kalTemperatura

	kalVlaznost = vlaznost / 24.7
	kalTemperatura = temperatura / 26.8

	led_r.off()
	led_g.off()
	led_b.off()

	if (kalTemperatura < 20):
		led_b.on()
	elif (kalTemperatura >= 20) and (kalTemperatura < 30):
		led_g.on()
	else:
		led_r.on()


def index(request):
	merenje()
	strTemperatura = "{:.1f}".format(kalTemperatura)
	strVlaznost = "{:.0f}".format(kalVlaznost)

	template = loader.get_template('template.html')
	context = {
		'Temperatura' : strTemperatura,
		'Vlaznost' : strVlaznost
	}

	return HttpResponse(template.render(context, request))
