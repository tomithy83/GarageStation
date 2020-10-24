'''relay > gpiopin
1 > 26
2 > 19
3 > 13
4 > 22
5 > 27
6 > 17
7 > 4
'''

import RPi.GPIO as GPIO
import time
relays = (26,21,19,20,16,13,6,12)

r1 = relays[0]
r2 = relays[1]
r3 = relays[2]
r4 = relays[3]
r5 = relays[4]
r6 = relays[5]
r7 = relays[6]
r8 = relays[7]

on = False
off = True

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(relays, GPIO.OUT)
GPIO.output(relays, off)


def testsequence1(delay):
    #turn each one on in turn
    GPIO.output(r1, on)
    time.sleep(delay)
    GPIO.output(r1, off)
    time.sleep(delay)

    GPIO.output(r2, on)
    time.sleep(delay)
    GPIO.output(r2, off)
    time.sleep(delay)

    GPIO.output(r3, on)
    time.sleep(delay)
    GPIO.output(r3, off)
    time.sleep(delay)

    GPIO.output(r4, on)
    time.sleep(delay)
    GPIO.output(r4, off)
    time.sleep(delay)

    GPIO.output(r5, on)
    time.sleep(delay)
    GPIO.output(r5, off)
    time.sleep(delay)

    GPIO.output(r6, on)
    time.sleep(delay)
    GPIO.output(r6, off)
    time.sleep(delay)

    GPIO.output(r7, on)
    time.sleep(delay)
    GPIO.output(r7, off)
    time.sleep(delay)
    
    GPIO.output(r8, on)
    time.sleep(delay)
    GPIO.output(r8, off)
    time.sleep(delay)

def testsequence2(delay):
    #first turn all on one at a time
    GPIO.output(r1, on)
    time.sleep(delay)
    GPIO.output(r2, on)
    time.sleep(delay)
    GPIO.output(r3, on)
    time.sleep(delay)
    GPIO.output(r4, on)
    time.sleep(delay)
    GPIO.output(r5, on)
    time.sleep(delay)
    GPIO.output(r6, on)
    time.sleep(delay)
    GPIO.output(r7, on)
    time.sleep(delay)
    GPIO.output(r8, on)
    time.sleep(delay)
    #then turn all off one at a time
    GPIO.output(r1, off)
    time.sleep(delay)
    GPIO.output(r2, off)
    time.sleep(delay)
    GPIO.output(r3, off)
    time.sleep(delay)
    GPIO.output(r4, off)
    time.sleep(delay)
    GPIO.output(r5, off)
    time.sleep(delay)
    GPIO.output(r6, off)
    time.sleep(delay)
    GPIO.output(r7, off)
    time.sleep(delay)
    GPIO.output(r8, off)
    time.sleep(delay)
    
def testsequence3(delay):
    #turn each one on in turn, reverse order
    GPIO.output(r8, on)
    time.sleep(delay)
    GPIO.output(r8, off)
    time.sleep(delay)

    GPIO.output(r7, on)
    time.sleep(delay)
    GPIO.output(r7, off)
    time.sleep(delay)

    GPIO.output(r6, on)
    time.sleep(delay)
    GPIO.output(r6, off)
    time.sleep(delay)

    GPIO.output(r5, on)
    time.sleep(delay)
    GPIO.output(r5, off)
    time.sleep(delay)

    GPIO.output(r4, on)
    time.sleep(delay)
    GPIO.output(r4, off)
    time.sleep(delay)

    GPIO.output(r3, on)
    time.sleep(delay)
    GPIO.output(r3, off)
    time.sleep(delay)

    GPIO.output(r2, on)
    time.sleep(delay)
    GPIO.output(r2, off)
    time.sleep(delay)

    GPIO.output(r1, on)
    time.sleep(delay)
    GPIO.output(r1, off)
    time.sleep(delay)

def testsequence4(delay):
    #first turn all on one at a time
    GPIO.output(r8, on)
    time.sleep(delay)
    GPIO.output(r7, on)
    time.sleep(delay)
    GPIO.output(r6, on)
    time.sleep(delay)
    GPIO.output(r5, on)
    time.sleep(delay)
    GPIO.output(r4, on)
    time.sleep(delay)
    GPIO.output(r3, on)
    time.sleep(delay)
    GPIO.output(r2, on)
    time.sleep(delay)
    GPIO.output(r1, on)
    time.sleep(delay)
    #then turn all off one at a time
    GPIO.output(r8, off)
    time.sleep(delay)
    GPIO.output(r7, off)
    time.sleep(delay)
    GPIO.output(r6, off)
    time.sleep(delay)
    GPIO.output(r5, off)
    time.sleep(delay)
    GPIO.output(r4, off)
    time.sleep(delay)
    GPIO.output(r3, off)
    time.sleep(delay)
    GPIO.output(r2, off)
    time.sleep(delay)
    GPIO.output(r1, off)
    time.sleep(delay)

def test():
    while True:
        testsequence1(0.5)
        testsequence2(0.1)
        testsequence3(0.25)
        testsequence4(0.75)
        testsequence2(0.5)
        testsequence3(0.1)
        testsequence4(0.25)
        testsequence1(0.75)
        testsequence3(0.5)
        testsequence4(0.1)
        testsequence1(0.25)
        testsequence2(0.75)
        testsequence4(0.5)
        testsequence1(0.1)
        testsequence2(0.25)
        testsequence3(0.75)

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        test()
    except KeyboardInterrupt:
        GPIO.output(relays, off)
        GPIO.cleanup()
        exit()