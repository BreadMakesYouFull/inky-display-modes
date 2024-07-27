from setuptools import setup, find_packages
setup(
    name = 'inkyfuncmap',
    packages = find_packages(),
    install_requires=[
        "bs4",
        # Saturated Palette in InkyMockImpression not reachable.
        # https://github.com/pimoroni/inky/issues/196
        "inky==1.3.2",
        "RPi.GPIO",
        "pillow",
        "requests",
        "uploadserver",
    ]
)
