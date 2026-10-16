const test = require("node:test"),
  assert = require("node:assert/strict");
global.RecipeCore = require("../js/core.js");
const C = RecipeCore,
  S = require("../js/state.js"),
  recipes = require("../data/recipes.json");
test("explicit taxonomy remains independent from incidental description words", () => {
  const expected = {
    "01": "postres",
    "02": "guarniciones",
    "03": "cenas",
    "04": "tecnicas",
    "05": "postres",
    "06": "comidas",
    "07": "cenas",
    "08": "comidas",
  };
  for (const r of recipes) {
    assert.equal(r.categoryId, expected[r.id]);
    assert(
      C.matches(
        { ...r, short: r.short + " airfryer cena fria" },
        { category: r.categoryId },
      ),
    );
  }
});
test("search combines terms and ignores negative advice", () => {
  const chocolate = recipes[0],
    salad = recipes.find((r) => r.id === "06");
  assert(!C.matches(chocolate, { q: "cena" }));
  assert(C.matches(salad, { q: "pollo patata" }));
  assert(
    C.matches(
      chocolate,
      { q: "proteico chocolate", favorite: true, status: "vista" },
      { favorite: true, status: "vista" },
    ),
  );
  assert(!C.matches(chocolate, { favorite: true }, { favorite: false }));
  assert.equal(C.normalize("VÍDEO frío"), "video frio");
});
test("legacy progress migrates by stable snapshot, not current ordering", () => {
  const reordered = structuredClone(recipes);
  reordered[0].steps.reverse();
  const data = S.migrate(
    {
      "01": {
        favorite: true,
        status: "cocinada",
        checkedSteps: [0, 2, 999],
        checkedIngredients: [1],
      },
    },
    reordered,
  );
  assert.deepEqual(data.recipes["01"].steps, ["paso-01", "paso-03"]);
  assert.deepEqual(data.recipes["01"].ingredients, ["ing-02"]);
  assert(data.recipes["01"].favorite);
});
test("invalid state and denied storage leave usable transient state", () => {
  let warned = false;
  const store = S.create(
    {
      getItem() {
        throw Error();
      },
      setItem() {
        throw Error();
      },
    },
    recipes,
    () => (warned = true),
  );
  store.entry("01").favorite = true;
  assert.equal(store.save(), false);
  assert(store.entry("01").favorite);
  assert(warned);
  assert.throws(() => S.validate({ version: 4, recipes: [] }, recipes));
  assert.throws(() => store.preview("{bad"));
});
test("legacy data survives migration and malformed checks are rejected", () => {
  const data = new Map([
    [S.OLD, JSON.stringify({ "01": { checkedSteps: [0], status: "vista" } })],
  ]);
  const store = S.create(
    { getItem: (k) => data.get(k), setItem: (k, v) => data.set(k, v) },
    recipes,
  );
  assert(data.has(S.OLD));
  assert(data.has(S.KEY));
  assert.equal(store.entry("01").status, "vista");
  const validated = S.validate(
    {
      version: 4,
      recipes: {
        "01": { steps: ["paso-01", "bad", "paso-01"], status: "invalid" },
      },
    },
    recipes,
  );
  assert.deepEqual(validated.recipes["01"].steps, ["paso-01"]);
  assert.equal(validated.recipes["01"].status, "pendiente");
});
test("absolute timer recovers elapsed wall clock and never shows negative time", () => {
  const timer = { state: "running", endsAt: 61000 };
  assert.equal(C.remaining(timer, 1000), 60);
  assert.equal(C.remaining(timer, 58000), 3);
  assert.equal(C.remaining(timer, 90000), 0);
  assert.equal(C.formatTime(480 * 60), "8:00:00");
  assert.equal(C.formatTime(-1), "0:00");
});
test("import validates timer limits and known recipe timer IDs", () => {
  const state = S.validate(
    {
      version: 4,
      recipes: {},
      timers: {
        "01-reloj-1": { state: "paused", remaining: 10 },
        evil: { state: "running", endsAt: 1, remaining: 10 },
        "02-reloj-1": { state: "paused", remaining: Infinity },
      },
    },
    recipes,
  );
  assert.deepEqual(Object.keys(state.timers), ["01-reloj-1"]);
});
