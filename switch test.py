import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pin = 21
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO21


try:
    while True:
         button_state = "off" if GPIO.input(pin) else "on"
         print(f"switch status is {button_state}")
         time.sleep(0.5)

except:
    GPIO.cleanup()