const test = require("node:test"),
  assert = require("node:assert/strict"),
  vm = require("node:vm"),
  fs = require("node:fs");
const core = require("../js/core.js");
test("timer persists across controller recreation, expires once, and requires explicit reset", () => {
  let now = 100000,
    tick,
    saves = 0,
    announcements = 0;
  const events = [];
  const context = vm.createContext({
    window: {},
    RecipeCore: { ...core, remaining: (t) => core.remaining(t, now) },
    Date: { now: () => now },
    setInterval: (fn) => {
      tick = fn;
      return 1;
    },
    clearInterval() {},
    Event: class {
      constructor(type) {
        this.type = type;
      }
    },
    document: {
      addEventListener() {},
      removeEventListener() {},
      dispatchEvent: (e) => events.push(e.type),
    },
  });
  vm.runInContext(fs.readFileSync("js/timers.js", "utf8"), context);
  const store = {
    state: { timers: {}, sound: false },
    save() {
      saves++;
    },
  };
  let controller = context.window.createRecipeTimers(
    store,
    () => announcements++,
  );
  controller.act("01-reloj-1", "start", 60);
  assert.equal(store.state.timers["01-reloj-1"].endsAt, 160000);
  controller.destroy();
  now += 45000;
  controller = context.window.createRecipeTimers(store, () => announcements++);
  assert.equal(core.remaining(store.state.timers["01-reloj-1"], now), 15);
  now += 20000;
  tick();
  tick();
  assert.equal(store.state.timers["01-reloj-1"].state, "done");
  assert.equal(events.length, 1);
  controller.act("01-reloj-1", "start", 60);
  assert.equal(store.state.timers["01-reloj-1"].state, "done");
  controller.act("01-reloj-1", "reset", 60);
  assert.equal(store.state.timers["01-reloj-1"].state, "paused");
  controller.act("01-reloj-1", "resume", 60);
  now += 10000;
  controller.act("01-reloj-1", "pause", 60);
  assert.equal(store.state.timers["01-reloj-1"].remaining, 50);
  assert(saves >= 5);
  assert(announcements >= 5);
});
