from sys import stderr
from os import environ
from threading import Thread
from time import sleep
from enum import StrEnum
from typing import Union

if environ.get("SEMAFOR_GPIO_ENABLE", "0") == "1":
    from gpiozero import LED


LIGHT_COLORS = ["red", "yellow", "green"]


class LEDState(StrEnum):
    ON = "on"
    OFF = "off"
    BLINK = "blink"


class MockLED:
    def __init__(self, name: str):
        self.name = name

    def on(self):
        print(f"{repr(self)}.on()")

    def off(self):
        print(f"{repr(self)}.off()")

    def toggle(self):
        print(f"{repr(self)}.toggle()")

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name})"


class LEDController:
    def __init__(self):
        self.lights = {color: LEDState.OFF for color in LIGHT_COLORS}
        self._prev_lights = dict(self.lights)

        self._leds = {
            color: self._gpio_or_mock(f"SEMAFOR_GPIO_{color.upper()}")
            for color in LIGHT_COLORS
        }

        self._runtime_thread = Thread(
            name="Semafor GPIO Control Thread",
            target=self._thread_main,
        )

    def start(self):
        self._runtime_thread.start()

    @staticmethod
    def _gpio_or_mock(env_pin: str) -> Union[MockLED, "LED"]:
        if environ.get("SEMAFOR_GPIO_ENABLE", "0") != "1":
            return MockLED(env_pin)

        try:
            pin = int(environ[env_pin])
        except KeyError:
            print(
                f"{env_pin} is not set. Defaulting to virtual LED.",
                file=stderr,
            )
            return MockLED(env_pin)
        except ValueError as e:
            print(
                f"Value for {env_pin} is invalid: {str(e)}",
                file=stderr,
            )
            return MockLED(env_pin)

        return LED(pin)

    def _thread_main(self):
        print("started LEDController thread")
        while True:
            self._update_pins()
            self._blink_leds()
            sleep(0.5)

    def _update_pins(self):
        if self._prev_lights == self.lights:
            return

        for color in LIGHT_COLORS:
            if self.lights[color] == LEDState.OFF:
                self._leds[color].off()
            else:
                self._leds[color].on()  # blink starts with on

        self._prev_lights = dict(self.lights)

    def _blink_leds(self):
        for color, state in self.lights.items():
            if state == LEDState.BLINK:
                self._leds[color].toggle()
