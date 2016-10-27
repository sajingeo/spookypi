### The awesome halloween script
### Author : Sajin George sajin.geo@gmail.com
### credits briandconnelly

import pywink
import lifxlan
import pygame
import os
import sys
import time
import requests

CLIENT_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
EMAIL = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
PWD = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
IFTTT_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxx"

BLUE = [43634, 65535, 65535, 3500]
COLD_WHITE = [58275, 0, 65535, 9000]
BLACK = [0, 0, 0, 0]
ORANGE = [5525, 65535, 65535, 3500]

THUNDERSTORM_SLEEPS= [0.2,0.2,0.5,0.2,0.2]

pywink.set_wink_credentials(EMAIL,PWD,CLIENT_ID,CLIENT_SECRET) ##WINK
lifx = Lifx.LAN() ##lifx
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
	for bulb in bulbs: ## save current brightness
		initial_brightness.append(bulb.brightness())

	for bulb in bulbs: ## turn off main lights
		bulb.set_state(False,brightness=0)

	##play spooky music
	pygame.mixer.music.load("spooky.wav")
	pygame.mixer.play()

	## start with a blue glow on lifx
	lifx.set_color_all_lights_color(BLUE,duration = 15)
	time.sleep (60)

	while pygame.mixer.music.get_busy() == True:
    	continue ## wait for spooky move to get over

	##play lightning
	##play thunder
	thunder()
	pygame.mixer.music.load("thunder.wav")
	pygame.mixer.play()

	## play spooky music
	pygame.mixer.music.load("spooky.wav")
	pygame.mixer.play()

	#turn on TV
	trigger_ifttt("spooky")
	while pygame.mixer.music.get_busy() == True:
    	continue

	##wait for 30 secs
	time.sleep(30)

	##play lightning
	##play thunder
	thunder()
	pygame.mixer.music.load("thunder.wav")
	pygame.mixer.play()
	while pygame.mixer.music.get_busy() == True:
    	continue ## wait for thunder to be over

	##turn off TV
	trigger_ifttt("spookend")

	## play music
	## restore house
	pygame.mixer.music.load("spooky.wav")
	pygame.mixer.play()
	while pygame.mixer.music.get_busy() == True:
    	continue

    pygame.mixer.music.load("spooky.wav")
	pygame.mixer.play() ## play screeming lady!!

	for index,bulb in enumerate(bulbs): ## restore home lights
		bulb.set_state(initial_brightness[index])

	## set color back to orange
	lifx.set_color_all_lights_color(ORANGE,duration = 15)
	

def thunder():
	thunder = 4
	selector = True
	while(thunder > 0):
		if (selector):
			selector = False
			lifx.set_color_all_lights_color(COLD_WHITE,rapid = True)
		else:
			selector = True
			lifx.set_color_all_lights_color(BLACK,rapid = True)

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
