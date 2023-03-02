import RPi.GPIO as GPIO
from time import sleep  # For pausing

GPIO.setmode(GPIO.BCM)  # BCM numbering, not BOARD
GPIO.setup(5, GPIO.IN)  # Sets pin4 to an input

try:  # Doesn't kill the program on an error, goes to finally instead
    while True:  # MASH CTRL+C to stop the program

        if GPIO.input(5):  # Checks what's up with Pin 4, if it's TRUE or FALSE
            print("I'm reading TRUE on GPIO 5")

        else:
            print("I'm reading FALSE on GPIO 5")

        sleep(1)  # Wait 1 second before the next reading

finally:  # When you CTL+C out of the try block, you end up here

    print("Cleaning up...")
    GPIO.cleanup()  # Turns off all pins that are still on so the next program runs cleanly