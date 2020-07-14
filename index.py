#import modules:
from flask import Flask, render_template, redirect, url_for, request
import datetime
import RPi.GPIO as GPIO
import time

#create app object
app = Flask(__name__)

#setup relays
relays = (26,19,13,22,27,17,4,0)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(relays, GPIO.OUT)


#make human-readable variables
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
doordelay = 0.5 #time in seconds to press the button to open the garage door. 

GPIO.output(relays, off)

#define the home page
@app.route('/')
def home():
    #get the date and time
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M:%S")
    
    #read the relay states
    #GPIO.output(r1, on) #used for testing
    r1_state = 'on' if GPIO.input(r1) == 0 else'off'
    r2_state = 'on' if GPIO.input(r2) == 0 else'off' 
    r3_state = 'on' if GPIO.input(r3) == 0 else'off'
    r4_state = 'on' if GPIO.input(r4) == 0 else'off'
    r5_state = 'on' if GPIO.input(r5) == 0 else'off'
    r6_state = 'on' if GPIO.input(r6) == 0 else'off'
    r7_state = 'on' if GPIO.input(r7) == 0 else'off'
    r8_state = 'on' if GPIO.input(r8) == 0 else'off'
    
    #set theparamaters to copy to the template 
    templateData = {
        'title' : 'Garage Station',
        'time' : timeString,
        'r1_state' : r1_state,
        'r2_state' : r2_state,
        'r3_state' : r3_state,
        'r4_state' : r4_state,
        'r5_state' : r5_state,
        'r6_state' : r6_state,
        'r7_state' : r7_state,
        'r8_state' : r8_state
        }
    return render_template('Station.html', **templateData)

#define the garage door sequences
@app.route('/<garagedoor>')
def actuatedoor(garagedoor):
    if garagedoor == 'door1':
        relay = r1
    if garagedoor == 'door2':
        relay = r2
    if garagedoor == 'bothdoors':
        relay = [r1,r2]
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
    if circuit == 'r1':
        relay =r1
    elif circuit == 'r2':
        relay =r2
    elif circuit == 'r3':
        relay =r3
    elif circuit == 'r4':
        relay =r4
    elif circuit == 'r5':
        relay =r5
    elif circuit == 'r6':
        relay =r6
    elif circuit == 'r7':
        relay =r7
    elif circuit == 'r8':
        relay =r8
    elif circuit == 'all_lights':
        relay = relays[2:8]
    else:
        return redirect(url_for('home'))
    #set the GPIO pin   
    GPIO.output(relay, state)
    time.sleep(doordelay)
    return redirect(url_for('home'))

#start server
if __name__ == '__main__':
    app.run(debug=True)