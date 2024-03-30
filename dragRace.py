# drag strip (python + pigpio)

import pigpio
import time

ON = 1
OFF = 0

pi = pigpio.pi()

# TODO: set correct pin numbers
# 1 button, 4 lasers, 2 green leds, 6 yellow leds, 2 red leds
buttonPin = 0
laserPins = [0, 0, 0, 0]
ledPins = {
	"green": [0, 0],
	"yellow": [0, 0, 0, 0, 0, 0],
	"red": [0, 0]	
}

# Set up
pi.set_mode(buttonPin, pigpio.INPUT)

for pin in laserPins:
	pi.set_mode(pin, pigpio.INPUT)
 
for colors in ledPins.values():
	for pin in colors:
		pi.set_mode(pin, pigpio.OUTPUT)

# check if a car moves out of position during the countdown
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
 
	# time each car with lasers at the end of the track
	startTime = time.time()
	leftCarFinished = false
	rightCarFinished = false
	while not leftCarFinished or not rightCarFinished: # wait for both cars to finish the race
		if pi.read(laserPins[2]) == 1 and not leftCar:
			if not rightCarFinished:
				print("Left car wins!")
			print("Left car time: " + str(time.time() - startTime))
			leftCarFinished = true
		if pi.read(laserPins[3]) == 1 and not rightCar:
			if not leftCarFinished:
				print("Right car wins!")
			print("Right car time: " + str(time.time() - startTime))
			rightCarFinished = true
		time.sleep(0.01)

def main():
	# wait for button to be pressed
	while True:
		print("wait for button press...")
		if pi.read(buttonPin) == 1 and all(pi.read(laserPins) == 1 for pin in laserPins):
			startRace()
		elif pi.read(buttonPin) == 1:
			print("car(s) not in position")
		time.sleep(0.1)
