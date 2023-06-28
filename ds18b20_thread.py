import time
import RPi.GPIO as GPIO
import w1thermsensor
import threading
import queue

sensor = w1thermsensor.W1ThermSensor()
temp_queue = queue.Queue()

def temp():
    while True:
        temperatura = sensor.get_temperature()
        # print(temperatura)
        temp_queue.put(temperatura)
        time.sleep(1)

temp_thread = threading.Thread(target=temp, )
temp_thread.start()

while(True):
    read = temp_queue.get(block=False)
    print(read)


print("hello")



