# Bootloader for Ben Eater's 8-bit Computer

Because I'm sick of DIP switches.

When powered on, connects to the Wi-Fi, pulls down a program, loads it
into RAM, hits reset and (optionally) starts the clock.

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

## Installing

Update bootloader.py to specify your SSID, Wi-Fi password and URL.

This is what I did to load it on my board:

```bash
sudo pip3 install git+https://github.com/natemueller/ampy.git@96936f946a32fba8d89c5607fb60e2cef83f4f1a
esptool.py --port /dev/tty.usbserial-0001 -c esp32 erase_flash
esptool.py --port /dev/tty.usbserial-0001 -c esp32 write_flash -z 0x1000 ~/Downloads/esp32-idf4-20200902-v1.13.bin
ampy --port /dev/tty.usbserial-0001 put bootloader.py main.py
```

## Program Format

Program files can be up to 16 bytes in length, big-endian.  If the
file is less than 16 bytes, the remaining memory addresses will be
initialized to zero.

The stupid-simple `asm.rb` assembler will generate files in the right
format.
