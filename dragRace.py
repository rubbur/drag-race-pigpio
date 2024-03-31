# drag strip (python + pigpio)

from sense_hat import SenseHat
import time

ON = 1
OFF = 0

sense = SenseHat()
sense.clear()

red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)

# 1 button, 4 lasers, 2 green leds, 8 yellow leds, 2 red leds
buttonPin = 2
#laserPins = [3, 4, 5, 6]
leftLaser = 1
rightLaser = 1

# check if a car moves out of position during the countdown
def checkFoul():
	if leftLaser == 1:
		sense.set_pixel(0, 0, red)
	if rightLaser == 1:
		sense.set_pixel(7, 0, red)
		
	"""
	if pi.read(laserPins[0]) == 1:
		pi.write(ledPins["red"][0], ON)
	if pi.read(laserPins[1]) == 1:
		pi.write(ledPins["red"][1], ON)
	"""
 
def flashLeds(pins, color):
	print("turning on pins: " + str(pins))
	for pin in pins:
		sense.set_pixel(pin[0][0], pins[0][1], color)
		sense.set_pixel(pins[1][0], pins[1][1], color)
	time.sleep(0.5)
	for pin in pins:
		sense.set_pixel(pins[0][0], pins[0][1], black)
		sense.set_pixel(pins[1][0], pins[1][1], black)
	checkFoul()

def startRace():
	flashLeds([[0, 0], [7, 0]], yellow)
	flashLeds([[0, 0], [7, 0]], yellow)
	flashLeds([[0, 0], [7, 0]], yellow)
	flashLeds([[0, 0], [7, 0]], yellow)
	startTime = time.time()
	leftCarFinished = False
	rightCarFinished = False
	while not leftCarFinished or not rightCarFinished: # wait for both cars to finish the race
		"""if pi.read(laserPins[2]) == 1 and not leftCarFinished:
			if not rightCarFinished:
				print("Left car wins!")
			print("Left car time: " + str(time.time() - startTime))
			leftCarFinished = True
		if pi.read(laserPins[3]) == 1 and not rightCarFinished:
			if not leftCarFinished:
				print("Right car wins!")
			print("Right car time: " + str(time.time() - startTime))
			rightCarFinished = True
		"""
		time.sleep(0.01)

def main():
	# wait for button to be pressed
	while True:
		input("Press Enter to start...")
		#if pi.read(buttonPin) == 1 and pi.read(laserPins[0]) == 0 and pi.read(laserPins[1]) == 0:
		startRace()
		#elif pi.read(buttonPin) == 1:
		#	print("car(s) not in position")
		time.sleep(0.1)

if __name__ == "__main__":
	main()
    