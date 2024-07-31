"""inkyfuncmap function implementation.
"""

import glob
import os
import random
import subprocess
import textwrap
import time

from PIL import Image, ImageFont, ImageDraw
import inky
import requests
import threading

from . import config


IMG_DIR=os.getenv("INKY_IMG_DIR", os.path.join(os.getcwd(), "img"))
"""Random image directory.
"""


def __null_function(*args, **kwargs):
    """No registered function found."""
    pass


def text(display=None, text=None, center=True):
    """Draw text on screen

    Args:
        display (Inky or InkyMock): to draw image to
        text (str): Text to display

    Returns:
        Inky or InkyMock: Display that has been drawn to
    """
    font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 20)
    image = Image.new("RGB", (display.width, display.height), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.multiline_text(
        (
            10,
            10 + int(int(center) * ((display.height * 0.5) - len(text.split("\n"))*10))
        ),
        text,
        font=font,
        fill=(255, 255, 255)
    )
    display.set_border(inky.BLACK)
    display.set_image(image)
    display.show()
    return image


def hello_world(display=None):
    """Draw hello world on screen

    Args:
        display (Inky or InkyMock): to draw image to.

    Returns:
        Inky or InkyMock: Display that has been drawn to.
    """
    return text(display=display, text="Hello world!")    


def random_image_from(display=None, dir=IMG_DIR):
    """Draw a random image on screen.

    Args:
        display (Inky or InkyMock): to draw image to.
        dir (str): image directory path.

    Returns:
        Inky or InkyMock: Display that has been drawn to.
    """
    print(f"image search path {dir}")
    img = random.choice(
        glob.glob(os.path.join(dir, "./*.jpg"))
      + glob.glob(os.path.join(dir, "./*.jpeg"))
      + glob.glob(os.path.join(dir, "./*.JPG"))
      + glob.glob(os.path.join(dir, "./*.JPEG"))
      + glob.glob(os.path.join(dir, "./*.png"))
      + glob.glob(os.path.join(dir, "./*.PNG"))
        or [None]
    )
    if img:
        with Image.open(img) as image:
            background = Image.new("RGBA", (600, 448))
            if image.width > image.height:
                print(display.width, int(image.height * display.width / image.width))
                image = image.resize((display.width, int(image.height * display.width / image.width)))
                offset = (0, (background.height - image.height) // 2)
            else:
                print((int(image.width * display.height / image.height)), display.height)
                image = image.resize((int(image.width * display.height / image.height), display.height))
                offset = ((background.width - image.width) // 2, 0)
            background.paste(image, offset)
            display.set_image(background)
            display.show()
            return background

def random_image(display=None):
    """Draw a random image on screen from default directory.

    Args:
        display (Inky or InkyMock): to draw image to.

    Returns:
        Inky or InkyMock: Display that has been drawn to.
    """
    random_image_from(display=display, dir=IMG_DIR)


def hackaday_news(display=None):
    """Draw hackaday news on screen from rss feed.

    Args:
        display (Inky or InkyMock): to draw image to.

    Returns:
        Inky or InkyMock: Display that has been drawn to.
    """
    import os
    import subprocess
    import textwrap
    import requests
    cmd = "curl -s 'https://hackaday.com/blog/feed/' | grep -Eo '<title>(.*)>' | grep -v Hackaday | sed -e 's/<title>//' -e 's|</title>||' -e 's/&.*;//g'"
    text = _run_bash(cmd)
    if text:
        text = "\n".join(textwrap.wrap(text.replace("\n", "  //  "), width=30))
        image = Image.new("RGBA", (600, 448), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 30)
        draw.multiline_text((10, 15), "HACKADAY NEWS", font=font, fill=(255, 255, 255))
        font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 30)
        draw.multiline_text((20, 80), text, font=font, fill=(255, 255, 255))
        display.set_border(inky.BLACK)
        display.set_image(image)
        display.show()
        return image


def noise(display=None):
    """Draw a random noise on screen.

    Args:
        display (Inky or InkyMock): to draw image to.

    Returns:
        Inky or InkyMock: Display that has been drawn to.
    """
    image = Image.new("RGB", (display.width, display.height))
    rgb_pixels = (
        (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))
        for x in range(image.width)
        for y in range(image.height)
    )
    image.putdata(list(rgb_pixels))
    print("setting")
    display.set_image(image)
    print("show")
    display.show()
    return image


def nasa(display=None):
    """Draw a random image from nasa on screen

    Args:
        display (Inky or InkyMock): to draw image to.

    Returns:
        Inky or InkyMock: Display that has been drawn to.
    """
    retry = 3
    for i in range(retry):
        try:
            from bs4 import BeautifulSoup
            import requests
            import datetime
            url = "https://apod.nasa.gov/apod/ap{}.html".format("{:02}{:02}{:02}".format(random.randint(15,23), random.randint(1,12), random.randint(1,28)))
            print(url)
            page = requests.get(url)
            soup = BeautifulSoup(page.content)
            images = soup.findAll('img')
            url = "https://apod.nasa.gov/apod/" + images[0]["src"]
            img_data = requests.get(url).content
            with open('/tmp/inkyfuncmapnasa.png', 'wb') as handler:
                handler.write(img_data)
            with Image.open("/tmp/inkyfuncmapnasa.png") as image:
                image = image.resize((display.width, display.height))
                display.set_image(image)
                display.show()
                return image
        except:
            pass


def _run_bash(cmd):
    """Run bash command.
    """
    print(cmd)
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
    print(output)
    return output


def bash(cmd):
    """bash function factory.

    Args:
        cmd (str): bash command to run
    Returns:
    function: to call with display
    """
    return lambda display: text(display, _run_bash(cmd))


def switch_func(display, increment):
    """Change display index.
    """
    display.index += increment
    print("mode " + config.FUNC_KEYS[display.index])
    # Also ensure no auto thread running:
    if hasattr(display, "stop_auto") and display.stop_auto:
        display.stop_auto.set()


def reset(display):
    """Reset display to first index.
    """
    display.index = 0


def menu(display):
    """List available modes."""
    text(
        display,
        "\n".join(
            [
                f"{i: 2}) {config.FUNC_KEYS[i]}"
                for i in range(len(config.FUNC_KEYS))
            ]
        )
    )


def auto(display, func, refresh=60 * 60):
    """Auto refresh another function.

    Set ``refresh`` seconds, default hourly.
    """
    def _auto(display, func, refresh):
        print("auto running: {}".format(func))
        while not display.stop_auto.is_set():
            print("calling: {}".format(func))
            func(display)
            time.sleep(refresh)  # minimum screen time
        print("Auto run stopped.")
    display.stop_auto = threading.Event()
    thread = threading.Thread(target=lambda: _auto(display, func, refresh))
    thread.start()
