### The awesome halloween script
### Author : Sajin George sajin.geo@gmail.com
### credits briandconnelly

import pywink
from lifxlan import *
import pygame
import os
import sys
import time
import requests
import subprocess

CLIENT_ID = "xxxxxxxxxxxxxxxxxxxxxxx"
CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
EMAIL = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
PWD = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
IFTTT_KEY = "xxxxxxxxxxxxxxxxxxxxxx"

BLUE = [43634, 65535, 32767, 3500]
COLD_WHITE = [58275, 0, 65535, 9000]
BLACK = [0, 0, 0, 0]
ORANGE = [5525, 65535, 32767, 3500]

THUNDERSTORM_SLEEPS= [0.1,0.1,0.1,0.1,0.1]

DEVNULL = open(os.devnull, 'wb')

pywink.set_wink_credentials(EMAIL,PWD,CLIENT_ID,CLIENT_SECRET) ##WINK
lifx = LifxLAN(2) ##lifx
pygame.mixer.init() ##music

def trigger_ifttt(event="spooky"):
	"""Send an event to the IFTTT maker channel"""
	url = "https://maker.ifttt.com/trigger/{e}/with/key/{k}/".format(e=event,
																	 k=IFTTT_KEY)
	payload = {'value1': 0, 'value2': 0, 'value3': 0}
	return requests.post(url, data=payload)

def loop():
	initial_brightness = []
	bulbs = pywink.get_bulbs()

	for bulb in bulbs: ## turn off main lights
		bulb.set_state(False,brightness=0)

	##play spooky music
	ps1 = subprocess.Popen(["exec omxplayer -o local spooky.wav"],stdout=DEVNULL,shell=True)

	## start with a blue glow on lifx
	lifx.set_color_all_lights(BLUE,duration = 15)
	time.sleep (15)

	ps1.kill()## wait for spooky move to get over

	##play lightning
	##play thunder
	ps2 = subprocess.Popen(["exec omxplayer -o local thunder.wav"],stdout=DEVNULL,shell = True)
	thunder()
	ps2.kill()

	## play spooky music
	trigger_ifttt("spooky")
	ps3 = subprocess.Popen(["exec omxplayer -o local spooky.wav"],stdout=DEVNULL,shell = True)
	lifx.set_color_all_lights(BLUE,duration = 15)
	time.sleep(15)
	ps3.kill()

	##wait for 30 secs
	time.sleep(15)

	##play lightning
	##play thunder
	ps4 = subprocess.Popen(["exec omxplayer -o local thunder.wav"],stdout=DEVNULL,shell = True)
	thunder()
	ps4.kill()


	lifx.set_color_all_lights(BLUE,duration = 15)
	## play music
	## restore house
	ps5 = subprocess.Popen(["exec omxplayer -o local spooky.wav"],stdout=DEVNULL,shell = True)
	time.sleep(10)
	
	##turn off TV
	trigger_ifttt("spookend")
	
	ps5.kill()

	ps6 = subprocess.Popen(["exec omxplayer -o local scream.wav"],stdout=DEVNULL,shell = True)
	time.sleep(2)
	ps6.kill()

	bulbs = pywink.get_bulbs()
	bulbs[0].set_state(True,0.04)
	bulbs[1].set_state(True,0.04)

	## set color back to orange
	lifx.set_color_all_lights(ORANGE,duration = 15)
	os.system('killall omxplayer.bin')
	

def thunder():
	thunder = 4
	selector = True
	lifx.set_power_all_lights("on")
	while(thunder > 0):
		if (selector):
			selector = False
			lifx.set_color_all_lights(COLD_WHITE,rapid = True)
		else:
			selector = True
			lifx.set_color_all_lights(BLACK,rapid = True)
		thunder = thunder - 1
		time.sleep(THUNDERSTORM_SLEEPS[thunder])


def screen_init():
	pygame.init()
	screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
	screen.fill((255, 255, 255))
	pygame.display.update()

	font = pygame.font.SysFont('freeserif', 38, bold=1)
	text = ":)  SMILE   NOW   !!  " + str(timeDelay) 
	textSurface = font.render(text, 1, pygame.Color(255, 255, 255))
	textSurface = pygame.transform.rotate(textSurface,90)
	screen.blit(textSurface, (400, 80))
	# finally update and display the image
	pygame.display.update()

def detect_mouse_click():
	ev = pygame.event.get()
	# proceed events
	for event in ev:
		# handle MOUSEBUTTONUP
		if event.type == pygame.MOUSEBUTTONDOWN:
			loop()



def main():
	print "starting spookyness..."
	while (True):
		loop()
		time.sleep(60)

if __name__ == "__main__":
	main()
