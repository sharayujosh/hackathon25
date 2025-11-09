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

print("Clock started. Press SET to enter adjust mode.")

while clock.second < 10:
    try:
        clock.tick()
        send_byte(0x80)
        lcd_write("Time: {:02d}:{:02d}:{:02d}".format(clock.hour, clock.minute, clock.second))
        if (clock.second <= 1):           
            try:
                print("Playing sound.wav...")
                for i in range(clock.hour):
                    play_wav("Goose.wav")
                print("played")
            finally:
                pwm.deinit()
                print("Done.")
        send_byte(0xC0)  # Move cursor to line 2
        lcd_write("Goose")
        sleep(1)  # sleep 1 sec
    except KeyboardInterrupt:
        break      

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
