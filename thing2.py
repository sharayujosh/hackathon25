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
from machine import Pin, PWM
from time import sleep
import struct
# import os

# # List files
# print(os.listdir())  # Shows files on the Pico's flash

# # Delete a file
# filename = "sound.wav"
# if filename in os.listdir():
#     os.remove(filename)
#     print(f"{filename} deleted")
# else:
#     print(f"{filename} not found")

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

try:
    print("Playing sound.wav...")
    play_wav("Goose.wav")
    print("played")
finally:
    pwm.deinit()
    print("Done.")

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

# ---- Main Program ----
# Define pin connections
RS = Pin(16, Pin.OUT)
E  = Pin(17, Pin.OUT)
D4 = Pin(18, Pin.OUT)
D5 = Pin(19, Pin.OUT)
D6 = Pin(20, Pin.OUT)
D7 = Pin(21, Pin.OUT)

print("pins defined")
lcd_init()
print("pins intitalized 2")
lcd_write("Hello, world!")
send_byte(0xC0)  # Move cursor to line 2
lcd_write("Line two here")