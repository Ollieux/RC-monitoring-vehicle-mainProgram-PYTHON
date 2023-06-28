import time
import RPi.GPIO as GPIO
import w1thermsensor
import threading

sensor = w1thermsensor.W1ThermSensor()

def temp():
    while True:
        temperatura = sensor.get_temperature()
        print(temperatura)
        time.sleep(1)

temp_thread = threading.Thread(target=temp, )
temp_thread.start()


print("hello")



