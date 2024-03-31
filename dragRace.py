from sense_hat import SenseHat
import tkinter as tk
import time
import threading

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
leftLaser = True
rightLaser = True

# GUI
root = tk.Tk()
root.title("Tree Window")

canvas = tk.Canvas(root, width=600, height=600)
CELL_SIZE = 75

for i in range(8):
    for j in range(8):
        x0, y0 = j * CELL_SIZE, i * CELL_SIZE
        x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
        canvas.create_rectangle(x0, y0, x1, y1, fill="black", outline="")

def update_pixel(row, col, color):
    x0, y0 = col * CELL_SIZE, row * CELL_SIZE
    x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

update_pixel(0, 0, "green")

def gui_thread():
    root.mainloop()

def sense_thread():
    def checkFoul():
        if leftLaser:
            sense.set_pixel(6, 0, red)
        if rightLaser:
            sense.set_pixel(6, 7, red)
            
    def flashLeds(pins, color):
        print("turning on pins: " + str(pins))
        for pin in pins:
            sense.set_pixel(pins[0][0], pins[0][1], color)
            sense.set_pixel(pins[1][0], pins[1][1], color)
        time.sleep(0.5)
        for pin in pins:
            sense.set_pixel(pins[0][0], pins[0][1], black)
            sense.set_pixel(pins[1][0], pins[1][1], black)
        checkFoul()
     
    def stageOn():
        sense.set_pixel(0, 6, yellow)
        sense.set_pixel(0, 7, yellow)
        time.sleep(0.5)  
        sense.set_pixel(0, 0, yellow)
        sense.set_pixel(0, 1, yellow)
        time.sleep(0.5)
        sense.set_pixel(1, 6, yellow)
        sense.set_pixel(1, 7, yellow)
        time.sleep(0.5)
        sense.set_pixel(1, 0, yellow)
        sense.set_pixel(1, 1, yellow)
        time.sleep(0.5)

    def stageOff():
        sense.set_pixel(0, 6, black)
        sense.set_pixel(0, 7, black)
        sense.set_pixel(0, 0, black)
        sense.set_pixel(0, 1, black)
        sense.set_pixel(1, 6, black)
        sense.set_pixel(1, 7, black)
        sense.set_pixel(1, 0, black)
        sense.set_pixel(1, 1, black)

    def startRace():
        stageOn()
     
        flashLeds([[2, 0], [2, 7]], yellow)
        flashLeds([[3, 0], [3, 7]], yellow)
        flashLeds([[4, 0], [4, 7]], yellow)
        if leftLaser:
            sense.set_pixel(5, 0, green)
        if rightLaser:
            sense.set_pixel(5, 7, green)
      
        stageOff()
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
            break
        time.sleep(3)
        sense.clear()

    while True:
        global leftLaser, rightLaser
        while True:
            userInput = input("\npress 1 to toggle laser1, currently: {}\npress 2 to toggle laser2, currently: {}\npress enter to start\n\nInput: ".format(leftLaser, rightLaser))
            if userInput == '1':
                leftLaser = not leftLaser
                print("laser1 is now: {}".format(leftLaser))
            elif userInput == '2':
                rightLaser = not rightLaser
                print("laser2 is now: {}".format(rightLaser))
            elif userInput == "":
                break
        startRace()
        time.sleep(0.1)

sense_thread = threading.Thread(target=sense_thread)
sense_thread.start()

# Run the GUI in the main thread
gui_thread()
