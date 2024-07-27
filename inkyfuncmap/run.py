"""inkyfuncmap

Run mock or real inky display.

Buttons are mapped as 1, 2, 3, 4, to functions.

To configure function mappings modify ``config.py``

If you use a different display to UC8159 "Inky Impression",
you may need to adapt these scripts.
"""

import glob
import random
import signal
import subprocess
import sys
import threading

from PIL import Image, ImageFont, ImageDraw
import inky
import inky.mock
import requests

from . import config
from . import func


def start_display():
    """Startup a display.

    Will attempt to connect to hardware display and fallback to mock.

    Returns:
        Inky or InkyMock: Display accepting ``set_draw(PIL.Image)`` and ``show()``.
    """
    try:
        display = inky.auto()
        print("Hardware display")
    except RuntimeError:
        display = inky.mock.InkyMockImpression()
        print("Mock display")
        # Empty window title
        display.tk_root.title("")

    print("Display detected: {}".format(display.resolution))

    # Force full saturation
    display._set_image = display.set_image
    def __set_image_full_saturation(img, saturation=1.0):
        """use full saturation by default, and store last image."""
        display.last_image = img
        display._set_image(img, saturation)
    display.set_image = __set_image_full_saturation
    return display

def _tk_keypress(display, event):
    """Handle tk keypress events.

    Map ``event.char`` to mapped function of ``config.KEYS``.

    Args:
        event (tkinter.Event): keypress event.
    """
    print(event.char)
    function = config.KEYS.get(event.char, func.__null_function)
    thread = threading.Thread(target=lambda: function(display))
    thread.start()
    #return function(display)


def _inky_keypress(display, pin):
    """Handle button events.

    Map ``event.char`` to mapped function of ``config.KEYS``.

    Args:
        display (inky.Inky): draw display
        pin (int): gpio pin press
    """
    label = config.LABELS[config.BUTTONS.index(pin)]
    print("Button press detected on pin: {} label: {}".format(pin, label))
    function = config.KEYS.get(label.lower(), func.__null_function)
    thread = threading.Thread(target=lambda: function(display))
    thread.start()
    #return function(display)


def main():
    """Main entry.

    Run mock or real inky impression display.

    To configure function mappings modify ``config.py``
    """
    global display
    display = start_display()
    display.index = 0
    if isinstance(display, inky.mock.InkyMock):  # mocked
        # Register keyboard events
        display.tk_root.bind("<KeyPress>", lambda event: _tk_keypress(display, event))
        config.FUNCS[config.FUNC_KEYS[display.index]](display)
        # Display GUI
        display.tk_root.mainloop()
    else:  # Raspi / inky display
        import RPi.GPIO as GPIO
        # Set up RPi.GPIO with the "BCM" numbering scheme
        GPIO.setmode(GPIO.BCM)
        # Buttons connect to ground when pressed, so we should set them up
        # with a "PULL UP", which weakly pulls the input signal to 3.3V.
        GPIO.setup(config.BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)    
        # Loop through out buttons and attach the "handle_button" function to each
        # We're watching the "FALLING" edge (transition from 3.3V to Ground) and
        # picking a generous bouncetime of 250ms to smooth out button presses.
        for pin in config.BUTTONS:
            GPIO.add_event_detect(pin, GPIO.FALLING, lambda pin: _inky_keypress(display, pin), bouncetime=250)
        # Finally, since button handlers don't require a "while True" loop,
        # we pause the script to prevent it exiting immediately.
        signal.pause()


if __name__ == "__main__":
    sys.exit(main())
