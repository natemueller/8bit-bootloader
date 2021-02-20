import sys
import time
import network
import urequests
from machine import Pin

SSID = ""
PASSWORD = ""
PROGRAM_URL = ""
WRITE_DELAY_MS = 500
AUTO_START = True

STATUS_LEDS = list(map(lambda p: Pin(p, Pin.OUT), [27, 14, 12, 13]))
ADDR_LINES = list(map(lambda p: Pin(p, Pin.OUT), [23, 22, 1, 21]))
DATA_LINES = list(map(lambda p: Pin(p, Pin.OUT), [19, 18, 5, 17, 16, 4, 2, 15]))
WRITE_ENABLE = Pin(33, Pin.OUT, value=1)
RESET = Pin(32, Pin.OUT)
PROGRAM_MODE = Pin(25, Pin.OUT)
CLOCK_MODE = Pin(26, Pin.IN)

# ESP32 booted and we're in the bootloader program
STATUS_LEDS[0].on()
print("Booted")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep_ms(100)
        pass

# Connected to Wi-Fi
STATUS_LEDS[1].on()
print("Connected to Wi-Fi")

resp = urequests.get(PROGRAM_URL)
if resp.status_code != 200:
    print("Failed to download:", resp.content)
    sys.exit()

program_data = list(resp.content)
resp.close()

if len(program_data) > 16:
    sys.exit()

# Downloaded the program and it looks valid
STATUS_LEDS[2].on()
print("Program downloaded:", program_data)

print("Programming...")
for addr in range(0, 16):
    if addr >= len(program_data):
        data = 0
    else:
        data = program_data[addr]

    print("  {0:04b} {1:08b}".format(addr, data))

    for bit in range(0, 4):
        ADDR_LINES[3 - bit].value((addr >> bit) & 1)

    for bit in range(0, 8):
        DATA_LINES[7 - bit].value((data >> bit) & 1)

    time.sleep_ms(10)

    WRITE_ENABLE.off()
    time.sleep_ms(10)
    WRITE_ENABLE.on()

    time.sleep_ms(WRITE_DELAY_MS)

RESET.on()
time.sleep_ms(10)
RESET.off()

list(map(lambda p: p.init(p.IN), ADDR_LINES))
list(map(lambda p: p.init(p.IN), DATA_LINES))
WRITE_ENABLE.init(WRITE_ENABLE.IN)
PROGRAM_MODE.init(PROGRAM_MODE.IN)
RESET.init(RESET.IN)

if AUTO_START:
    CLOCK_MODE.init(CLOCK_MODE.OUT, value=0)
    time.sleep_ms(100)
    CLOCK_MODE.init(CLOCK_MODE.IN)

# Everything is programmed
STATUS_LEDS[3].on()
print("Done")
