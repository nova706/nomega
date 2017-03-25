from time import *
from OmegaExpansion import onionI2C


class I2cDevice:
    def __init__(self, address, port=0):
        self.address = address
        self.i2c = onionI2C.OnionI2C(port)

    # Write a single command
    def write_cmd(self, cmd):
        self.i2c.write(self.address, [cmd])
        sleep(0.0001)

    # Write a command and argument
    def write_cmd_arg(self, cmd, data):
        self.i2c.writeByte(self.address, cmd, data)
        sleep(0.0001)

    # Write a block of data
    def write_block_data(self, cmd, data):
        self.i2c.writeBytes(self.address, cmd, [data])
        sleep(0.0001)

    # Read a single byte
    #   def read(self):
    #      return self.bus.read_byte(self.address)
    #
    # Read
    #   def read_data(self, cmd):
    #      return self.i2c.readBytes(self.address, cmd,1)
    #
    # Read a block of data
    #   def read_block_data(self, cmd):
    #      return self.i2c.readBytes(self.address, cmd)
