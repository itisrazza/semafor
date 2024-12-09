# Copyright (C) 2024 Raresh Nistor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

    if LEDState(body["state"]) not in LEDState:
        return abort(400)

    if body.get("exclusive", False) is True:
        for light in LIGHT_COLORS:
            led_controller.lights[light] = LEDState.OFF

    led_controller.lights[body["color"]] = LEDState(body["state"])
    print(led_controller.lights)

    return ""
