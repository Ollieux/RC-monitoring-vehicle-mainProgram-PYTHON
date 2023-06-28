import time
import RPi.GPIO as GPIO
import w1thermsensor

sensor = w1thermsensor.W1ThermSensor()

while True:
    temperatura = sensor.get_temperature()
    print(temperatura)

    # time.sleep(0.1)