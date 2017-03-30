# Python Scripts
Python scripts for the Omega 2

## Get Started

1. Install [Onion I2C Python Library](https://wiki.onion.io/Documentation/Libraries/I2C-Python-Module)
```sh
opkg update
opkg install git git-http python pyOnionI2C
```

2. Clone the GitHub project
```sh
cd /root
git clone https://github.com/nova706/nomega.git
cd nomega
```

## LCD CLI Usage

### Options:

* ``-h, --help`` show the help message and exit
* ``-a ADDRESS, --address=ADDRESS`` the I2C Address (0x3f by default)
* ``-p, --persistent`` do not clear display before new write
* ``--line1=LINE1`` text to line 1
* ``--line2=LINE2`` text to line 2
* ``--line3=LINE3`` text to line 3
* ``--line4=LINE4`` text to line 4
* ``--backlight-off`` turn off backlight for this write

### Example:
```sh
python py/lcd.py -a 0x3f --line1="Onion LCD LIB" --line2="Hello World"
```

### Troubleshooting:

* Make sure to tune the contrast of the LCD
* The default address for the LCD is 0x3f. This may not be the correct address for your LCD. You can use i2cTools to determine the address of your LCD. Below, i2cdetect is showing an address of 0x3f for the LCD.
```sh
i2cdetect -y 0
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 3f
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```
> My Omega 2 never seemed to show me the address. I still don't fully understand this. By default the LCD that ships with the starter kit is at address 0x3f.

## Onion Cloud Usage

* The file exec command can be used to call the CLI scripts directly
```sh
curl -H "Content-Type: application/json" -H "X-API-KEY: <Your_Api_Key>" -X POST -d '{"command":"python","params":["/root/nomega/py/lcd.py","--line1=Hello World"],"env":""}' https://api.onion.io/v1/devices/<Your_Device_ID>/file/exec
```
> Obviously this is not very elegant. I'm still trying to find a way to call the REST interface more directly

## TODO

* Add service interface to allow more direct REST calls to the tools
* Allow the LCD driver to take a single string and break it as needed to fit the screen
* Add scrolling text to the options to the LCD driver
* Keep adding more utilities