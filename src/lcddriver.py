import i2c_lib
from time import *

# commands
LCD_CLEAR_DISPLAY = 0x01
LCD_RETURN_HOME = 0x02
LCD_ENTRY_MODE_SET = 0x04
LCD_DISPLAY_CONTROL = 0x08
LCD_CURSOR_SHIFT = 0x10
LCD_FUNCTION_SET = 0x20
LCD_SET_CGRAMA_DDR = 0x40
LCD_SET_DDRAM_ADDRESS = 0x80

# flags for display entry mode
LCD_ENTRY_RIGHT = 0x00
LCD_ENTRY_LEFT = 0x02
LCD_ENTRY_SHIFT_INCREMENT = 0x01
LCD_ENTRY_SHIFT_DECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAY_ON = 0x04
LCD_DISPLAY_OFF = 0x00
LCD_CURSOR_ON = 0x02
LCD_CURSOR_OFF = 0x00
LCD_BLINK_ON = 0x01
LCD_BLINK_OFF = 0x00

# flags for display/cursor shift
LCD_DISPLAY_MOVE = 0x08
LCD_CURSOR_MOVE = 0x00
LCD_MOVE_RIGHT = 0x04
LCD_MOVE_LEFT = 0x00

# flags for function set
LCD_8BIT_MODE = 0x10
LCD_4BIT_MODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NO_BACKLIGHT = 0x00

En = 0b00000100  # Enable bit
Rw = 0b00000010  # Read/Write bit
Rs = 0b00000001  # Register select bit


class Lcd:

    # Initializes objects and lcd. If not supplied, uses default address 0x3f
    def __init__(self, address='0x3f'):
        self.address = int(address, 0)
        self.lcd_device = i2c_lib.I2cDevice(self.address)

        # lcd default status
        self.lcdBacklight = LCD_BACKLIGHT
        self.line1 = ""
        self.line2 = ""
        self.line3 = ""
        self.line4 = ""

        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)

        self.lcd_write(LCD_FUNCTION_SET | LCD_2LINE | LCD_5x8DOTS | LCD_4BIT_MODE)
        self.lcd_write(LCD_DISPLAY_CONTROL | LCD_DISPLAY_ON)
        self.lcd_write(LCD_CLEAR_DISPLAY)
        self.lcd_write(LCD_ENTRY_MODE_SET | LCD_ENTRY_LEFT)
        sleep(0.2)

    # Creates an EN pulse (using I2C) to latch previously sent command
    def lcd_strobe(self, data):
        self.lcd_device.write_cmd(data | En | self.lcdBacklight)
        sleep(.0005)
        self.lcd_device.write_cmd(((data & ~ En) | self.lcdBacklight))
        sleep(.0001)

    def lcd_write_four_bits(self, data):

        # write four data bits along with backlight state to the screen
        self.lcd_device.write_cmd(data | self.lcdBacklight)

        # perform strobe to latch the data that was sent
        self.lcd_strobe(data)

    # Write an 8-bit command to lcd
    def lcd_write(self, cmd, mode=0):

        # Due to how the I2C backpack expects data, send the top four and bottom four bits of the command separately
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    # Display a string on a specified line of the screen
    def lcd_display_string(self, string, line):
        if line == 1:
            self.line1 = string
            self.lcd_write(0x80)
        if line == 2:
            self.line2 = string
            self.lcd_write(0xC0)
        if line == 3:
            self.line3 = string
            self.lcd_write(0x94)
        if line == 4:
            self.line4 = string
            self.lcd_write(0xD4)

        for char in string:
            self.lcd_write(ord(char), Rs)

    # Display a list of strings on the LCD
    def lcd_display_string_list(self, strings):
        for x in range(0, min(len(strings), 4)):
            self.lcd_display_string(strings[x], x + 1)

    # Clear lcd and set to home
    def lcd_clear(self):
        self.lcd_write(LCD_CLEAR_DISPLAY)
        self.lcd_write(LCD_RETURN_HOME)

    def refresh(self):
        self.lcd_display_string(self.line1, 1)
        self.lcd_display_string(self.line2, 2)
        self.lcd_display_string(self.line3, 3)
        self.lcd_display_string(self.line4, 4)

    # Turn on the backlight
    def backlight_on(self):
        self.lcdBacklight = LCD_BACKLIGHT
        self.refresh()

    # Turn off the backlight
    def backlight_off(self):
        self.lcdBacklight = LCD_NO_BACKLIGHT
        self.refresh()
