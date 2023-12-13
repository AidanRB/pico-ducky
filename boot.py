# License : GPLv2.0
# copyright (c) 2023  Dave Bailey
# Author: Dave Bailey (dbisu, @daveisu)
# Pico and Pico W board support

import board
import digitalio
import storage
import usb_midi
import usb_cdc
import usb_hid
import supervisor
import neopixel

# hide unnecessary USB devices
usb_midi.disable()
usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
    usb_hid.Device.CONSUMER_CONTROL)
)

# storage/serial logic
noStoragePin = digitalio.DigitalInOut(board.GP15)
noStoragePin.switch_to_input(pull=digitalio.Pull.UP)
noStorageStatus = noStoragePin.value

# If GP15 is not connected, it will default to being pulled high (True)
# If GP is connected to GND, it will be low (False)

# GP15 not connected == USB NOT visible
# GP15 connected to GND == USB visible

print("GP15", noStorageStatus)

# initialize LED
pixel = neopixel.NeoPixel(board.GP16, 1)
pixel[0] = (0, 0, 100) # GRB, blue
pixel.write()

if(noStorageStatus):
    # normal boot (hidden)
    storage.disable_usb_drive()
    usb_cdc.disable()
    supervisor.set_usb_identification(manufacturer=" ", product="Dell KB216 Wired Keyboard", vid=16700, pid=8467)
    print("Disabling USB drive")
else:
    # show USB drive to host PC
    print("USB drive enabled")
