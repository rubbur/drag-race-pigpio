# drag strip (python + pigpio)

import pigpio
import time

ON = 1
OFF = 0

pi = pigpio.pi()

buttonPin = 21
laserPins = []
ledPins = {
	"green": [],
	"yellow": [],
	"red": []	
}

# Set up
pi.set_mode(buttonPin, pigpio.INPUT)

for pin in laserPins:
	pi.set_mode(pin, pigpio.INPUT)
 
for colors in ledPins.values():
	for pin in colors:
		pi.set_mode(pin, pigpio.OUTPUT)

# Check if a car moves out of position during countdown
def checkFoul():
	if pi.read(laserPins[0]) == 0:
		pi.write(ledPins["red"][0], ON)
	if pi.read(laserPins[1]) == 0:
		pi.write(ledPins["red"][1], ON)

def flashLeds(pins):
	for pin in pins:
		pi.write(pin, ON)
	checkFoul()
	time.sleep(0.5)
	for pin in pins:
		pi.write(pin, OFF)
	checkFoul()

def startRace():
	flashLeds(ledPins["yellow"][0:2])
	flashLeds(ledPins["yellow"][2:4])
	flashLeds(ledPins["yellow"][4:6])
	pi.write(ledPins["green"][0], ON)
	pi.write(ledPins["green"][1], ON)

def main():
	# Wait for button to be pressed
	while True:
		print("wait for button press...")
		if pi.read(buttonPin) == 1 and all(pi.read(laserPins) == 1 for pin in laserPins):
			startRace()
		elif pi.read(buttonPin) == 1:
			print("car(s) not in position")
		time.sleep(0.1)
