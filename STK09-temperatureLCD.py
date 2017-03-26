import src.lcddriver
import src.oneWire
from src.temperatureSensor import TemperatureSensor

# default address of i2c backpack is 0x3f by default
lcdAddress = "0x3f"

# setup one wire temperature sensor object
oneWireGpio = 19  # set the GPIO that we've connected the sensor to
pollingInterval = 1  # seconds


# function to read the temperature from the One-Wire Temperature Sensor
def get_temp():
    # check if 1-Wire was setup in the kernel
    if not src.oneWire.setup_one_wire(str(oneWireGpio)):
        print "Kernel module could not be inserted. Please reboot and try again."
        return -1

    # get the address of the temperature sensor
    # it should be the only device connected in this experiment
    sensor_address = src.oneWire.scan_one_address()

    sensor = TemperatureSensor("oneWire", {"address": sensor_address, "gpio": oneWireGpio})
    if not sensor.ready:
        print "Sensor was not set up correctly. Please make sure that your sensor is firmly connected to the GPIO specified above and try again."
        return -1

    return sensor.readValue()


# function to display the temperature on the LCD screen
def display_temp(temp):
    # setup LCD
    lcd = src.lcddriver.Lcd(lcdAddress)
    lcd.backlight_on()

    lcd.lcd_display_string_list([
        "Temperature: ",
        str(temp) + " C"
    ])


def __main__():
    t = get_temp()
    display_temp(t)


if __name__ == '__main__':
    __main__()
