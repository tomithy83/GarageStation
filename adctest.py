import spidev, time
import math

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out

#temperature conversion from Celsius to Fahrenheit rounded to the nearest tenth  
def Fdeg(Cdeg):
    return round((Cdeg*9/5)+32,1)

class thermometer:
    thermometers = []
    
    def __init__(self,pin):
        thermometer.thermometers.append(self)
        self.pin = pin
        self.calculate()
        
    def calculate(self):
        self.value = analog_read(self.pin)        # read ADC value A0 pin
        self.voltage = self.value * 3.3 / 1024       # calculate voltage
        self.resistance = 10 * self.voltage / (3.3 - self.voltage)    # calculate resistance value of thermistor
        self.tempK = 1/(1/(273.15 + 25) + math.log(self.resistance/10)/3950.0) # calculate temperature (Kelvin)
        self.tempC = self.tempK -273.15        # calculate temperature (Celsius)
        self.tempF = Fdeg(self.tempC)     # calculate temperature (Fahrenheit)
        return self.tempF

#create thermometers
therm1 = thermometer(0)
therm2 = thermometer(1)
therm3 = thermometer(2)


while True:
#     reading = analog_read(0)
#     voltage = reading * 3.3 / 1024
    therm1.calculate()
    print(f"Therm 1: Reading = {therm1.value} \ Voltage = {round(therm1.voltage,3)} \ Temperature = {therm1.tempF}F")
    therm2.calculate()
    print(f"Therm 2: Reading = {therm2.value} \ Voltage = {round(therm2.voltage,3)} \ Temperature = {therm2.tempF}F")
    therm3.calculate()
    print(f"Therm 3: Reading = {therm3.value} \ Voltage = {round(therm3.voltage,3)} \ Temperature = {therm3.tempF}F")
    time.sleep(1)