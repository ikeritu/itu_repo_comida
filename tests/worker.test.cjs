const test = require("node:test"),
  assert = require("node:assert/strict"),
  vm = require("node:vm"),
  fs = require("node:fs");
function worker({ failInstall = false } = {}) {
  const handlers = {},
    deleted = [],
    stores = new Map();
  const mockCache = {
    addAll: async (list) => {
      assert(!list.some((s) => s.endsWith(".mp4")));
      if (failInstall) throw Error("network");
    },
    match: async () => null,
  };
  const caches = {
    open: async (name) => stores.get(name) || mockCache,
    keys: async () => [
      "another-app-v1",
      "recetario-video-lab-v3-8",
      "recetario-video-lab-media-v4",
    ],
    delete: async (name) => {
      deleted.push(name);
      return true;
    },
  };
  const self = {
    location: {
      href: "https://example.test/itu_repo_comida/service-worker.js",
    },
    addEventListener: (n, fn) => (handlers[n] = fn),
    clients: { claim: async () => {} },
    skipWaiting: () => {},
  };
  const context = vm.createContext({
    self,
    caches,
    URL,
    Response,
    Request,
    Blob,
    fetch: async () => new Response("network"),
    console,
    Set,
  });
  vm.runInContext(fs.readFileSync("service-worker.js", "utf8"), context);
  return { handlers, deleted, stores, context };
}
test("failed essential installation rejects and removes incomplete build", async () => {
  const w = worker({ failInstall: true });
  let promise;
  w.handlers.install({ waitUntil: (p) => (promise = p) });
  await assert.rejects(promise, /network/);
  assert(w.deleted[0].startsWith("recetario-video-lab-shell-"));
});
test("activation preserves unrelated caches and downloaded media", async () => {
  const w = worker();
  let promise;
  w.handlers.activate({ waitUntil: (p) => (promise = p) });
  await promise;
  assert.deepEqual(w.deleted, ["recetario-video-lab-v3-8"]);
});
test("cached video honors regular, suffix and invalid byte ranges", async () => {
  const w = worker(),
    video = vm.runInContext("Array.from(allowedVideos)[0]", w.context);
  w.stores.set("recetario-video-lab-media-v4", {
    match: async () =>
      new Response("0123456789", { headers: { "Content-Type": "video/mp4" } }),
  });
  for (const [range, status, body] of [
    ["bytes=2-5", 206, "2345"],
    ["bytes=-3", 206, "789"],
    ["bytes=8-", 206, "89"],
    ["bytes=99-", 416, ""],
    ["bytes=2-1", 416, ""],
  ]) {
    let response;
    w.handlers.fetch({
      request: new Request(video, { headers: { Range: range } }),
      respondWith: (p) => (response = p),
    });
    const r = await response;
    assert.equal(r.status, status);
    assert.equal(await r.text(), body);
  }
});
test("worker leaves non-GET and other subprojects untouched", () => {
  const w = worker();
  for (const request of [
    new Request("https://example.test/other/index.html"),
    new Request("https://example.test/itu_repo_comida/test", {
      method: "POST",
    }),
  ])
    w.handlers.fetch({
      request,
      respondWith() {
        assert.fail("Must not intercept");
      },
    });
});
test("navigation offline resolves index with query parameters", async () => {
  const w = worker();
  for (const cacheName of vm.runInContext("[SHELL]", w.context))
    w.stores.set(cacheName, {
      match: async (url) =>
        String(url).endsWith("index.html")
          ? new Response("offline shell")
          : null,
    });
  let promise;
  w.handlers.fetch({
    request: {
      method: "GET",
      url: "https://example.test/itu_repo_comida/?q=pollo",
      mode: "navigate",
    },
    respondWith: (p) => (promise = p),
  });
  assert.equal(await (await promise).text(), "offline shell");
});
