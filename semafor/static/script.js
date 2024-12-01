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
