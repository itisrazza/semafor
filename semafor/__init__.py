from os import environ
from dataclasses import dataclass
import json
from typing import Optional

from flask import Flask, render_template, request, abort, make_response

from .led import LEDController, LIGHT_COLORS, LEDState

app = Flask(__name__)

_led_controller_backing: Optional[LEDController] = None


def _led_controller() -> LEDController:
    global _led_controller_backing

    if _led_controller_backing is None:
        _led_controller_backing = LEDController()
        _led_controller_backing.start()

    return _led_controller_backing


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", lights=_led_controller().lights)


@app.route("/", methods=["POST"])
def update():
    body = json.loads(request.get_data())
    led_controller = _led_controller()

    if body["color"] not in LIGHT_COLORS:
        return abort(400)

    if body["state"] not in LEDState:
        return abort(400)

    if body.get("exclusive", False) is True:
        for light in LIGHT_COLORS:
            led_controller.lights[light] = LEDState.OFF

    led_controller.lights[body["color"]] = LEDState(body["state"])
    print(led_controller.lights)

    return ""
