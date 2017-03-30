# import modules and classes
import time

from src import oneWire
from src.temperatureSensor import TemperatureSensor

# setup onewire and polling interval
oneWireGpio = 19  # set the sensor GPIO
pollingInterval = 1  # seconds


def __main__():
    # check if 1-Wire is setup in the kernel
    if not oneWire.setup_one_wire(str(oneWireGpio)):
        print "Kernel module could not be inserted. Please reboot and try again."
        return -1

    # get the address of the temperature sensor
    #   it should be the only device connected in this experiment
    sensor_address = oneWire.scan_one_address()

    # instantiate the temperature sensor object
    sensor = TemperatureSensor("oneWire", {"address": sensor_address, "gpio": oneWireGpio})
    if not sensor.ready:
        print "Sensor was not set up correctly. Please make sure that your sensor is firmly connected to the GPIO specified above and try again."
        return -1

    # infinite loop - runs main program code continuously
    while 1:
        # check and print the temperature
        value = sensor.readValue()
        print "T = " + str(value) + " C"
        time.sleep(pollingInterval)


if __name__ == '__main__':
    __main__()
