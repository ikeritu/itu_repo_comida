(function () {
  "use strict";
  window.createRecipeTimers = function (store, onChange) {
    let audio;
    function notify() {
      if (!store.state.sound || !audio) return;
      try {
        const oscillator = audio.createOscillator(),
          gain = audio.createGain();
        oscillator.connect(gain);
        gain.connect(audio.destination);
        gain.gain.value = 0.12;
        oscillator.frequency.value = 880;
        oscillator.start();
        oscillator.stop(audio.currentTime + 0.6);
      } catch {}
    }
    function tick() {
      let changed = false;
      for (const timer of Object.values(store.state.timers)) {
        if (timer.state === "running" && RecipeCore.remaining(timer) === 0) {
          timer.state = "done";
          timer.remaining = 0;
          timer.acknowledged = false;
          changed = true;
          notify();
          document.dispatchEvent(new Event("recipe-timer-done"));
        }
      }
      if (changed) store.save();
      onChange();
    }
    const handle = setInterval(tick, 1000);
    document.addEventListener("visibilitychange", tick);
    return {
      act(key, action, seconds) {
        const timers = store.state.timers,
          timer = timers[key];
        if (action === "start" && !timer)
          timers[key] = {
            state: "running",
            endsAt: Date.now() + seconds * 1000,
            remaining: seconds,
            acknowledged: false,
          };
        if (action === "pause" && timer?.state === "running") {
          timer.remaining = RecipeCore.remaining(timer);
          timer.state = timer.remaining ? "paused" : "done";
        }
        if (action === "resume" && timer?.state === "paused") {
          timer.endsAt = Date.now() + timer.remaining * 1000;
          timer.state = "running";
        }
        if (action === "reset")
          timers[key] = {
            state: "paused",
            remaining: seconds,
            endsAt: 0,
            acknowledged: false,
          };
        if (action === "cancel") delete timers[key];
        if (action === "ack" && timer) timer.acknowledged = true;
        store.save();
        tick();
      },
      async sound(enabled) {
        store.state.sound = enabled;
        store.save();
        if (enabled) {
          try {
            audio ||= new (window.AudioContext || window.webkitAudioContext)();
            await audio.resume();
          } catch {}
        }
      },
      tick,
      destroy() {
        clearInterval(handle);
        document.removeEventListener("visibilitychange", tick);
      },
    };
  };
})();
