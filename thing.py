from machine import Pin
from gpio_lcd import GpioLcd
 
# Create the LCD object
lcd = GpioLcd(rs_pin=Pin(8),
              enable_pin=Pin(9),
              d4_pin=Pin(10),
              d5_pin=Pin(11),
              d6_pin=Pin(12),
              d7_pin=Pin(13),
              num_lines=2, num_columns=16)
 
# #The following line of codes should be tested using the REPL
#
# #1. To print a string to the lcd, you can use
lcd.putstr('Hello world!')