# Bootloader for Ben Eater's 8-bit Computer

Because I'm sick of DIP switches.

When powered on, this connects to the Wi-Fi, pulls down a program,
loads it into RAM, hits reset and (optionally) starts the clock.

This code makes a couple assumptions:
  * All address and data DIP switches are set to one.
  * RAM program mode is disabled.
  * The clock is in manual pulse mode, or that you're using [Dawid
    Buchwald's modified clock selector
    circuit](https://www.reddit.com/r/beneater/comments/eai6ke/issue_with_clock_kit_and_possible_solution_with/).
    The auto-start logic only works with the modified selector
    circuit.

Status LEDs show completion of boot, Wi-Fi association, download and
program load steps.

One of my goals was to preserve the manual program mode.  If that's
not important to you, you could replace the DIP switches with a pair
of 74LS164 shift registers and output serially from the ESP32.  That
would greatly simplify the wiring (six connections from the ESP32 vs
16) and let you use a more compact breakout board.

## Hardware

I used the [HiLegto
ESP-WROOM-32](https://www.amazon.com/dp/B0718T232Z) board.  It exposes
all of the ESP32's GPIO ports, and is narrow enough to fit on a
breadboard with one row of holes on each side.  Besides that, there's
nothing special about this particular board.  The code should work
anywhere.  But be aware that the mapping of GPIO port to breakout
board pin isn't standard.  If you use another board you won't be able
to copy my wiring.

## Software

Program files can be up to 16 bytes in length, big-endian.  If the
file is less than 16 bytes, the remaining memory addresses will be
initialized to zero.

The stupid-simple `8sm` assembler will generate files in the right
format.  See [fibonacci.8sm](fibonacci.8sm) for an example input file.

You can host the program files on any web server your bootloader can
reach.  I use a simple static file server on my laptop for
development.  This example assumes that you set `PROGRAM_URL` to
http://&lt;your IP&gt;:8000/a.out.

```bash
./8sm fibonacci.8sm
ruby -run -ehttpd . -p8000
```

## Installation

Update bootloader.py to specify your SSID, Wi-Fi password and program
URL.

This is what I did to load it on my board.  I'm using a Mac.  I assume
this is equally easy on Linux or Windows but I don't know the details.

```bash
wget https://micropython.org/resources/firmware/esp32-idf4-20200902-v1.13.bin
sudo pip3 install git+https://github.com/natemueller/ampy.git@96936f946a32fba8d89c5607fb60e2cef83f4f1a
esptool.py --port /dev/tty.usbserial-0001 -c esp32 erase_flash
esptool.py --port /dev/tty.usbserial-0001 -c esp32 write_flash -z 0x1000 esp32-idf4-20200902-v1.13.bin
ampy --port /dev/tty.usbserial-0001 put bootloader.py main.py
```

Note that I had to use a patched version of ampy to talk to the
MicroPython interpreter on the ESP-WROOM-32.  See
scientifichackers/ampy#19.  Depending on your OS or breakout board you
may not need to worry about this.
