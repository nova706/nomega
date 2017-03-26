import os
import subprocess
import time

# specify delay duration to be used in the program
setupDelay = 3

# variables to hold filesystem paths
oneWireDir = "/sys/devices/w1_bus_master1"
paths = {
    "slaveCount": oneWireDir + "/w1_master_slave_count",
    "slaves": oneWireDir + "/w1_master_slaves"
}


# a bunch of functions to be used by the OneWire class
# insert the 1-Wire kernel module
# it's also called a "module", but it's actually software for the Omega's firmware!
def insert_kernel_module(gpio):
    arg_bus = "bus0=0," + gpio + ",0"
    subprocess.call(["insmod", "w1-gpio-custom", arg_bus])


# check the filesystem to see if 1-Wire is properly setup
def check_file_system():
    return os.path.isdir(oneWireDir)


# function to setup the 1-Wire bus
def setup_one_wire(gpio):
    # check and retry up to 2 times if the 1-Wire bus has not been set up
    for i in range(2):
        if check_file_system():
            return True  # exits if the bus is setup
            # no else statement is needed after this return statement

        # tries to insert the module if it's not setup
        insert_kernel_module(gpio)
        # wait for a bit, then check again
        time.sleep(setupDelay)
    else:
        # could not set up 1-Wire on the gpio
        return False


# check that the kernel is detecting slaves
def check_slaves():
    with open(paths["slaveCount"]) as slaveCountFile:
        slave_count = slaveCountFile.read().split("\n")[0]

    if slave_count == "0":
        # slaves not detected by kernel
        return False
    return True


# check if a given address is registered on the bus
def check_registered(address):
    slave_list = scan_addresses()
    registered = False
    for line in slave_list:
        if address in line:
            registered = True
    return registered


# scan addresses of all connected 1-w devices
def scan_addresses():
    if not check_file_system():
        return False

    with open(paths["slaves"]) as slaveListFile:
        slave_list = slaveListFile.read().split("\n")
        # last element is an empty string due to the split
        del slave_list[-1]
    return slave_list


# use to get the address of a single connected device
def scan_one_address():
    addresses = scan_addresses()
    return addresses[0]


# class definition for one wire devices
class OneWire:
    def __init__(self, address, gpio=19):  # use gpio 19 by default if not specified
        self.gpio = str(gpio)
        self.address = str(address)
        self.slaveFilePath = oneWireDir + "/" + self.address + "/" + "w1_slave"
        self.setupComplete = self.__prepare()

    # prepare the object
    def __prepare(self):
        # check if the system file exists
        # if not, set it up, then check one more time
        if not setup_one_wire(self.gpio):
            print "Could not set up 1-Wire on GPIO " + self.gpio
            return False

        # check if the kernel is recognizing slaves
        if not check_slaves():
            print "Kernel is not recognizing slaves."
            return False

        # check if this instance's device is properly registered
        if not check_registered(self.address):
            # device is not recognized by the kernel
            print "Device is not registered on the bus."
            return False

            # the device has been properly set up
        return True

    # function to read data from the sensor
    def read_device(self):
        # read from the system file
        with open(self.slaveFilePath) as slave:
            message = slave.read().split("\n")
            # return an array of each line printed to the terminal
        return message
