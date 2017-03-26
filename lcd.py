from optparse import OptionParser
from types import NoneType

import src.lcddriver

# parse arguments
parser = OptionParser()
# parse values
parser.add_option("-a", "--address", action="store", dest="address",
                  help="I2C Address")

parser.add_option("-p", "--persistent", action="store_true", dest="persistent", default=False,
                  help="-p = do not clear display before new write")

parser.add_option("--line1", action="store", dest="line1",
                  help="text to line 1")

parser.add_option("--line2", action="store", dest="line2",
                  help="text to line 2")

parser.add_option("--line3", action="store", dest="line3",
                  help="text to line 3")

parser.add_option("--line4", action="store", dest="line4",
                  help="text to line 4")

parser.add_option("--backlight-off", action="store_true", dest="backlight_off", default=False,
                  help="Turn off backlight")

# parse arguments to values
(options, args) = parser.parse_args()

# process argument - address
lcd = src.lcddriver.Lcd(options.address)

# process argument - persistent
if not options.persistent:
    lcd.lcd_clear()

# process argument - backlight
if options.backlight_off:
    lcd.backlight_off()
else:
    lcd.backlight_on()

# process argument line 1-4
for num in range(1, 4):  # to iterate between lines 1 to 4
    try:
        getattr(options, "line%d" % num)
    except NameError:
        print "Line %d not set" % num
    except NoneType:
        print "Line %d noneType" % num
    else:
        if getattr(options, "line%d" % num) is not None and len(getattr(options, "line%d" % num)) > 0:
            lcd.lcd_display_string(getattr(options, "line%d" % num), num)
