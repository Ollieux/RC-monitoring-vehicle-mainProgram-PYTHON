import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import os

def button_callback(channel):
    print("Button was pushed!")
    os.system("sudo reboot")


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(18, GPIO.RISING, callback=button_callback)

message = input("Press enter to quit\n\n")
GPIO.cleanup()