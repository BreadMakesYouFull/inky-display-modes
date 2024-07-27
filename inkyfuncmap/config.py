"""inkyfuncmap config.

Maps buttons / keypresses to functions.
"""

import subprocess
import textwrap
import time

from . import func
from . import phrases

MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24


BUTTONS = [5, 6, 16, 24]
"""list(int): GPIO pins for each button.

* Configured for "inky impression".
* Gpio pins for each button (from top to bottom).
* 7-Colour (UC8159)
* resolution: 600x447
"""


LABELS = ['1', '2', '3', '4']
"""list(int): keypress/label corresponding to button presses.

* Configured for "inky impression".
* Map their functions via ``KEYS``.
"""


FUNCS = {
    "menu": func.menu,
    "image": func.random_image,
    "image (auto)": lambda display: func.auto(
        display,
        func.random_image,
        refresh=HOUR // 4,
    ),
    "cowsay": lambda display: func.bash("cowsay '{}'".format(phrases.random()))(display),
    "cowsay (auto)": lambda display: func.auto(
        display,
        lambda display: func.bash("cowsay '{}'".format(phrases.random()))(display),
        refresh=DAY,
    ),
    "hackaday": lambda display: func.auto(
        display,
        func.hackaday_news,
        refresh=DAY,
    ),
    "weather": lambda display: func.auto(
        display,
        func.bash('curl --silent wttr.in/?T 2>/dev/null | head -8'),
        refresh=DAY // 4,
    ),
    "nasa": lambda display: func.auto(
        display,
        func.nasa,
        refresh=DAY,
    ),
    "hello": func.hello_world,
    "ps": lambda display: func.auto(
        display,
        func.bash('ps -eo pid,pcpu,pmem,comm --sort -pcpu | head -20'),
        refresh=HOUR // 4,
    ),
    "uptime": lambda display: func.auto(
        display,
        func.bash('uptime -p'),
        refresh=HOUR,
    ),
    "fetch": func.bash('neofetch --stdout'),
    "fortune": lambda display: func.text(display, '\n'.join(textwrap.wrap(phrases.random(), width=48))),
    "noise": func.noise,
}
"""Functions

Available functions to run from ``func`` module.
"""
FUNC_KEYS = list(FUNCS)
"""Ordered Function mapping"""


KEYS = {
    # draw
    "1": lambda display: FUNCS[FUNC_KEYS[display.index]](display),
    # previous
    "2": lambda display: func.switch_func(display, -1 if display.index > 0 else 0),
    # next
    "3": lambda display: func.switch_func(display, 1 if display.index < len(FUNCS)-1 else 0),
    # reset
    "4": lambda display: func.reset(display) and FUNCS[FUNC_KEYS[display.index]](display),
}
"""Inky Impression or keyboard keymapping"""
