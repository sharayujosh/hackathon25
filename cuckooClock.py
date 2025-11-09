# from machine import Pin
# from utime import sleep

# pin = Pin("LED", Pin.OUT)

# print("LED starts flashing...")
# while True:
#     try:
#         pin.toggle()
#         sleep(1) # sleep 1sec
#     except KeyboardInterrupt:
#         break
# pin.off()
# print("Finished.")

print("start code")
from machine import Pin, PWM, Timer
from time import *
import struct

import os

class Clock:
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

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

clock = Clock(12, 0, 0)
# List files
print(os.listdir())  # Shows files on the Pico's flash

# Use PWM to simulate DAC output
AUDIO_PIN = 22
pwm = PWM(Pin(AUDIO_PIN))
pwm.freq(22050)  # base PWM frequency (fast enough for audio)

def play_wav(name):
    with open(name, "rb") as f:
        # Skip WAV header
        f.read(44)
        chunk = f.read(1024)
        while chunk:
            for byte in chunk:
                # Convert 8-bit sample (0–255) to 16-bit duty cycle
                pwm.duty_u16(byte << 8)
            chunk = f.read(1024)

def pulse_enable():
    E.value(1)
    sleep(0.001)
    E.value(0)
    sleep(0.001)

def send_nibble(data):
    D4.value((data >> 0) & 1)
    D5.value((data >> 1) & 1)
    D6.value((data >> 2) & 1)
    D7.value((data >> 3) & 1)
    pulse_enable()

def send_byte(data, char_mode=False):
    RS.value(char_mode)
    send_nibble(data >> 4)
    send_nibble(data & 0x0F)
    sleep(0.002)

# def init_lcd(self):
#     sleep(.020)
#     # Send 0x03 three times to reset
#     for _ in range(.003):
#         self._send_nibble(0x03)
#         sleep(5)
#     # Tell it to switch to 4-bit mode
#     self._send_nibble(0x02)
#     sleep(.001)

#     # Function set: 4-bit, 2-line, 5x8 font
#     self.command(0x28)
#     # Display on, cursor off, blink off
#     self.command(0x0C)
#     # Entry mode: increment cursor
#     self.command(0x06)
#     # Clear display
#     self.clear()

def lcd_init():
    sleep(0.05)
    send_nibble(0x03)
    sleep(0.005)
    send_nibble(0x03)
    sleep(0.001)
    send_nibble(0x03)
    send_nibble(0x02)  # Set to 4-bit mode

    send_byte(0x28)  # 4-bit, 2 line, 5x8 font
    send_byte(0x0C)  # Display ON, cursor OFF
    send_byte(0x06)  # Entry mode set
    send_byte(0x01)  # Clear display
    sleep(0.005)

def lcd_clear():
    send_byte(0x01)
    sleep(0.005)

def lcd_write(text):
    for char in text:
        send_byte(ord(char), True)

def show_time():
    modes = ["Time: ", "SET HOUR", "SET MIN"]
    lcd_write("Time: {:02d}:{:02d}:{:02d}".format(clock.hour, clock.minute, clock.second))

def check_buttons():
    global mode, hrs, min, last_set_press, last_incr_press

    # SET button — cycles between display/hour/minute
    if not set.value() and time.ticks_ms() - last_set_press > DEBOUNCE_MS:
        mode = (mode + 1) % 3
        last_set_press = time.ticks_ms()
        show_time()

    # INC button — changes current value in set mode
    if not incr.value() and time.ticks_ms() - last_incr_press > DEBOUNCE_MS:
        if mode == 1:
            hrs = (hrs + 1) % 24
        elif mode == 2:
            min = (min + 1) % 60
        last_incr_press = time.ticks_ms()
        show_time()

# if (clock.second <= 1):           
#     try:
#         print("Playing sound.wav...")
#         for i in range(clock.hour):
#             play_wav("Goose.wav")
#         print("played")
#     finally:
#         pwm.deinit()
#         print("Done.")
        
# ---- Main Program ----
# Define pin connections
RS = Pin(16, Pin.OUT)
E  = Pin(17, Pin.OUT)
D4 = Pin(18, Pin.OUT)
D5 = Pin(19, Pin.OUT)
D6 = Pin(20, Pin.OUT)
D7 = Pin(21, Pin.OUT)

# Button setup
set = Pin(0, Pin.IN, Pin.PULL_UP)
incr = Pin(1, Pin.IN, Pin.PULL_UP)

# Debounce settings
DEBOUNCE_MS = 200
last_set_press = 0
last_incr_press = 0

# Time variables
hrs = 12
min = 0
sec = 0

# Modes: 0=display, 1=set hour, 2=set minute
mode = 0

print("Clock started. Press SET to enter adjust mode.")

show_time()

while clock.second < 10:
    try:
        clock.tick()
        send_byte(0x80)
        show_time()
        send_byte(0xC0)  # Move cursor to line 2
        lcd_write("Goose")
        check_buttons()
        sleep(0.1)
        sleep(1)  # sleep 1 sec
    except KeyboardInterrupt:
        break        

# print("pins defined")
# lcd_init()
# print("pins intitalized 2")

# class Clock:
#     def __init__(self, hour=0, minute=0, second=0):
#         self.hour = hour
#         self.minute = minute
#         self.second = second

#     def tick(self):
#         self.second += 1
#         if self.second >= 60:
#             self.second = 0
#             self.minute += 1
#         if self.minute >= 60:
#             self.minute = 0
#             self.hour += 1
#         if self.hour >= 24:
#             self.hour = 0

# clock = Clock(12, 0, 0)

# while clock.second < 10:
#     try:
#         clock.tick()
#         send_byte(0x80)
#         lcd_write("Time: {:02d}:{:02d}:{:02d}".format(clock.hour, clock.minute, clock.second))
#         if (clock.second <= 1):           
#             try:
#                 print("Playing sound.wav...")
#                 for i in range(clock.hour):
#                     play_wav("Goose.wav")
#                 print("played")
#             finally:
#                 pwm.deinit()
#                 print("Done.")
#         send_byte(0xC0)  # Move cursor to line 2
#         lcd_write("Goose")
#         sleep(1)  # sleep 1 sec
#     except KeyboardInterrupt:
#         break
