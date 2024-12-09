// Copyright (C) 2024 Raresh Nistor
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

function getLight(light) {
  return document.querySelector(`[data-light='${light}']`);
}

const exclusiveModeToggle = document.getElementById("exclusive-mode");
function getExclusiveMode() {
  return exclusiveModeToggle.checked;
}

document.querySelectorAll(".switchers [data-color]").forEach((switcher) => {
  switcher.addEventListener("click", () => {
    const color = switcher.getAttribute("data-color");
    const state = switcher.getAttribute("data-state");
    const light = getLight(color);

    if (getExclusiveMode()) {
      document
        .querySelectorAll("[data-light]")
        .forEach((light) => light.setAttribute("data-state", "off"));
    }

    light.setAttribute("data-state", state);

    fetch("/", {
      method: "post",
      body: JSON.stringify({
        color,
        state,
        exclusive: getExclusiveMode(),
      }),
    });
  });
});
