#import modules:
from flask import Flask, render_template, redirect, url_for, request
import datetime
import RPi.GPIO as GPIO
import time
import math
from ADCDevice import *
from gpiozero import CPUTemperature
from slackbot.slackbot import *


on = False
off = True
doordelay = 0.5 #time in seconds to press the button to open the garage door.

#get the date and time
def gettime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

#create app object
app = Flask(__name__)

#setup relays
relaypins = (26,19,13,22,27,17,4,0)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(relaypins, GPIO.OUT)

#temperature conversion from Celsius to Fahrenheit rounded to the nearest tenth  
def Fdeg(Cdeg):
    return round((Cdeg*9/5)+32,1)

#make CPU temperature available  
def getcputemp():
    cpu = CPUTemperature()
    return Fdeg(cpu.temperature)
    

# Define an ADCDevice class object and setup the ADC
adc = ADCDevice()
def setupadc():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)
setupadc()

#define thermometer class
class thermometer:
    thermometers = []
    
    def __init__(self,pin):
        thermometer.thermometers.append(self)
        self.pin = pin
        self.calculate()
        
    def calculate(self):
        self.value = adc.analogRead(self.pin)        # read ADC value A0 pin
        self.voltage = self.value / 255.0 * 3.3        # calculate voltage
        self.resistance = 10 * self.voltage / (3.3 - self.voltage)    # calculate resistance value of thermistor
        self.tempK = 1/(1/(273.15 + 25) + math.log(self.resistance/10)/3950.0) # calculate temperature (Kelvin)
        self.tempC = self.tempK -273.15        # calculate temperature (Celsius)
        self.tempF = Fdeg(self.tempC)     # calculate temperature (Fahrenheit)
        return self.tempF

#create thermometers
therm1 = thermometer(0)
#therm2 = thermometer(1)
#therm3 = thermometer(2)
#therm4 = thermometer(3)
#therm5 = thermometer(4)
#therm6 = thermometer(5)
#therm7 = thermometer(6)
#therm8 = thermometer(7)

#define relay class
class relay:
    
    def __init__(self,pin):
        self.pin = pin
        self.calculate()
        
        
    def calculate(self):
        self.state = 'on' if GPIO.input(self.pin) == 0 else'off'
    
relays = {}
for i in range(len(relaypins)):
    name = 'r{}'.format(i+1)
    pin = relaypins[i]
    relays[name] = relays.get(name, relay(pin = pin))
    
#turn relays off
GPIO.output(relaypins, off)

#Define the function to clean up the program at the close.   
def destroy():
    adc.close()
    GPIO.cleanup()

#define the home page
@app.route('/')
def home():
    #loop thru the relays to update the variables
    for r in list(relays.values()):
        r.calculate()

    #loop thru the thermometers to update the variables
    for therm in thermometer.thermometers:
        therm.calculate()
 
    #set theparamaters to copy to the template 
    templateData = {
        'title' : 'Garage Station',
        'time' : gettime(),
        'r1_state' : relays['r1'].state,
        'r2_state' : relays['r2'].state,
        'r3_state' : relays['r3'].state,
        'r4_state' : relays['r4'].state,
        'r5_state' : relays['r5'].state,
        'r6_state' : relays['r6'].state,
        'r7_state' : relays['r7'].state,
        'r8_state' : relays['r8'].state,
        'cputemp'  : getcputemp(),
        'temp1'    : therm1.tempF
        }
    return render_template('Station.html', **templateData)

#define the garage door sequences
@app.route('/actuatedoor/<garagedoor>')
def actuatedoor(garagedoor):
    if garagedoor == 'bothdoors':
        allrelays = list(relays.keys())
        relay = []
        for r in allrelays[0:2]:
            relay.append(relays[r].pin) 
        slackmsg(f"both garage doors were just activated at {gettime()}.")
    elif garagedoor == 'r1' or 'r2':
        relay = relays[garagedoor].pin
        dname = "middle bay" if garagedoor == 'r1' else "big bay"
        slackmsg(f"the {dname} garage door just activated at {gettime()}.")

    else:
        return redirect(url_for('home'))        
    GPIO.output(relay, on)
    time.sleep(doordelay)
    GPIO.output(relay, off)
    return redirect(url_for('home'))

#define functions for turning lights on and off
@app.route('/circuit/<circuit>/<action>')
def switch(circuit, action):
    #convert action input so that the GPIO can be set 
    if action == 'on':
        state = 0
    elif action == 'off':
        state = 1
    else:
        return redirect(url_for('home'))
    #convert the circuit to the correct variable so that the GPIO can be set
    if circuit == 'all_lights':
        allrelays = list(relays.keys())
        relay = []
        for r in allrelays[2:8]:
            relay.append(relays[r].pin)     
    elif circuit == 'r1' or 'r2' or 'r3' or 'r4' or 'r5' or 'r6' or 'r7' or 'r8':
        relay = relays[circuit].pin
    else:
        return redirect(url_for('home'))
    #set the GPIO pin     
    GPIO.output(relay, state)
    slackmsg(f"somebody just turned {circuit} {action}.")
    time.sleep(doordelay)
    return redirect(url_for('home'))

#start server
if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()