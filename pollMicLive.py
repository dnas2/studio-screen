#!/usr/bin/python
import Adafruit_BBIO.GPIO as GPIO
import time
 
import web

PORT_NUMBER = 8081

urls = (
    '/miclive', 'miclive',
	'/irnnext', 'irnnext',
	'/irn', 'irn'
)

irnnexthour = 0
irnlastset = time.time()
app = web.application(urls, globals())

class miclive:
	
	#Handler for the GET requests
	def GET(self):
		GPIO.setup("P9_11", GPIO.IN) #AKA GPIO_30 see diagram at http://kilobaser.com/blog/2014-07-15-beaglebone-black-gpios

		newstate = 1 - GPIO.input("P9_11")
		json = '{ "micLiveState": ' + str(newstate) + '}'
		web.header('Access-Control-Allow-Origin', '*')

		GPIO.cleanup()
		return json

class irn:

	#Handler for pings from Steve's cron job to tell us that IRN is coming next
	global irnnexthour
	global irnlastset
	irnlastset = time.time()
	irnnexthour = 1
	return 'OK'

class irnnext:

	#Handler for requests from the clock, checking whether IRN is next
	global irnnexthour
	global irnlastset
	irnsetage = time.time() - irnlastset
	if irnsetage > 1800:
		#Steve last pinged over 1800 secs (30 mins) ago, so assume IRN isn't happening
		irnlastset = time.time()
		irnnexthour = 0
	json = '{"irn": ' + str(irnnexthour) + '}'
	web.header('Access-Control-Allow-Origin', '*')
	return json
		
if __name__ == '__main__':
    app.run()
