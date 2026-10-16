const test = require("node:test"),
  assert = require("node:assert/strict"),
  cp = require("node:child_process");
const current = require("../data/recipes.json");
test("all audited recipes retain original ingredients, steps and editorial caveats", () => {
  const original = JSON.parse(
    cp.execFileSync(
      "git",
      [
        "show",
        "c1d665bb11b0747e4cca82d74902ddca16b0b63c:data/recetas_video_lab_v3.json",
      ],
      { encoding: "utf8" },
    ),
  );
  assert.equal(current.length, original.length);
  for (const previous of original) {
    const recipe = current.find((r) => r.id === previous.id);
    assert(recipe);
    for (const key of [
      "title",
      "short",
      "confidence",
      "seasoning",
      "when_use",
      "when_not",
      "tips",
    ])
      assert.deepEqual(recipe[key], previous[key]);
    for (const key of ["steps", "ingredients"])
      assert.deepEqual(
        recipe[key].map((x) => x.text),
        previous[key],
      );
  }
});
