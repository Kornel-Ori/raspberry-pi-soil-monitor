import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

try:
    while True:
        print("Soil sensor:", GPIO.input(17))
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()