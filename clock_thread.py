from machine import Pin, I2C
import time
import _thread

# ======== LCD Library (HD44780 over I2C) ========
class I2cLcd:
    # LCD Commands
    LCD_CLR = 0x01
    LCD_HOME = 0x02
    LCD_ENTRY_MODE = 0x04
    LCD_DISPLAY_CTRL = 0x08
    LCD_FUNCTION_SET = 0x20
    LCD_SET_DDRAM = 0x80

    # Flags
    LCD_ENTRY_LEFT = 0x02
    LCD_DISPLAY_ON = 0x04
    LCD_2LINE = 0x08
    LCD_5x8DOTS = 0x00

    def __init__(self, i2c, addr, rows, cols):
        self.i2c = i2c
        self.addr = addr
        self.rows = rows
        self.cols = cols
        self.backlight = 0x08  # Backlight ON
        self._init_lcd()

    def _write_byte(self, data):
        self.i2c.writeto(self.addr, bytes([data | self.backlight]))

    def _send(self, data, mode=0):
        high = data & 0xF0
        low = (data << 4) & 0xF0
        self._write_4bits(high | mode)
        self._write_4bits(low | mode)

    def _write_4bits(self, data):
        self._write_byte(data | 0x04)  # Enable bit high
        time.sleep_us(500)
        self._write_byte(data & ~0x04)  # Enable bit low
        time.sleep_us(500)

    def _command(self, cmd):
        self._send(cmd, 0)

    def write_char(self, char):
        self._send(ord(char), 1)

    def write(self, string):
        for char in string:
            self.write_char(char)

    def clear(self):
        self._command(self.LCD_CLR)
        time.sleep_ms(2)

    def move_to(self, col, row):
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        self._command(self.LCD_SET_DDRAM | (col + row_offsets[row]))

    def _init_lcd(self):
        time.sleep_ms(50)
        self._write_4bits(0x30)
        time.sleep_ms(5)
        self._write_4bits(0x30)
        time.sleep_us(200)
        self._write_4bits(0x30)
        self._write_4bits(0x20)  # 4-bit mode

        self._command(self.LCD_FUNCTION_SET | self.LCD_2LINE | self.LCD_5x8DOTS)
        self._command(self.LCD_DISPLAY_CTRL | self.LCD_DISPLAY_ON)
        self._command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_LEFT)
        self.clear()

# Create struct with hour, minute, second
class Clock:
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.chime_hour = 0
        self.chime_minute = 0
        self.chime_second = 0

    def set_chime(self, hour, minute, second):
        self.chime_hour = hour
        self.chime_minute = minute
        self.chime_second = second

    def start_chime(self) -> bool:
        rc = True
        if self.chime_hour > 0:
            rc &= self.hour % self.chime_hour == 0
        if self.chime_minute > 0:
            rc &= self.minute % self.chime_minute == 0
        if self.chime_second > 0:
            rc &= self.second % self.chime_second == 0
        return rc

    def tick(self):
        self.second += 1
        if self.second >= 60:
            self.second = 0
            self.minute += 1
        if self.minute >= 60:
            self.minute = 0
            self.hour += 1
        if self.hour >= 24:
            self.hour = 0

def run_clock(my_clock):
    while True:
        my_clock.tick()
        if my_clock.start_chime():
            _thread.start_new_thread(blink_led, (Pin("LED", Pin.OUT), 5, 0.2))

        lcd.move_to(0, 0)
        lcd.write("Time: {:02d}:{:02d}:{:02d}".format(my_clock.hour, my_clock.minute, my_clock.second))
        time.sleep(1)  # sleep 1 sec

def blink_led(pin, num_blinks, delay):
    for _ in range(num_blinks):
        pin.on()
        time.sleep(delay)
        pin.off()
        time.sleep(delay)

# ======== Main Program ========
# Adjust pins and I2C ID for your Pico
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

# Scan for I2C devices
devices = i2c.scan()
if not devices:
    raise Exception("No I2C device found. Check wiring!")
lcd_addr = devices[0]

# Create LCD object for 16x2 display
lcd = I2cLcd(i2c, lcd_addr, 2, 16)

# Display text on two rows
lcd.move_to(0, 0)
lcd.write("Hello, World!")
lcd.move_to(0, 1)
lcd.write("MicroPython Pico")

my_clock = Clock(12, 0, 0)
my_clock.set_chime(0, 0, 5)

run_clock(my_clock)    
