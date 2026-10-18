import assert from "node:assert/strict";
import { readFileSync, existsSync } from "node:fs";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { calculateCosts } = require("../main.js");
const base = {
  orders: 100,
  average: 50000,
  commission: 10,
  delivery: 10000,
  other: 200000,
};
assert.deepEqual(calculateCosts(base), {
  state: "valid",
  turnover: 5000000,
  commission: 500000,
  delivery: 1000000,
  other: 200000,
  total: 1700000,
});
assert.equal(calculateCosts({ ...base, orders: 0 }).total, 200000);
assert.equal(calculateCosts({ ...base, commission: 0, delivery: 0, other: 0 }).total, 0);
assert.equal(calculateCosts({ ...base, commission: 100 }).commission, 5000000);
assert.equal(calculateCosts({ ...base, commission: 12.5, other: 0.5 }).total, 1625000.5);
for (const field of Object.keys(base)) {
  assert.equal(calculateCosts({ ...base, [field]: "" }).state, "empty");
  for (const bad of [-1, NaN, Infinity, "wrong"])
    assert.equal(calculateCosts({ ...base, [field]: bad }).state, "invalid");
}
for (const values of [
  { orders: 1.5 },
  { orders: 1000001 },
  { commission: 100.1 },
  { average: 1e10 },
  { other: 1e13 },
])
  assert.equal(calculateCosts({ ...base, ...values }).state, "invalid");
function checkHTML(html, lang) {
  assert.ok(html.includes(`<html lang="${lang}">`));
  assert.equal((html.match(/<h1\b/g) || []).length, 1);
  for (const id of ['how','calculator','demo','product','telegram','management','features','start','pricing','faq','contacts'])
    assert.ok(html.includes(`id="${id}"`), `missing section ${id}`);
  assert.equal((html.match(/<details>/g) || []).length, html.includes('id="lead-form"')?9:10);
  for (const pattern of [
    /149.?000/,
    /299.?000/,
    /499.?000/,
    /без комисси/i,
    /7 заказов/,
    /24 часа/,
    /free trial/i,
  ])
    assert.ok(!pattern.test(html), "unconfirmed claim");
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map((m) => m[1]);
  assert.equal(new Set(ids).size, ids.length);
  for (const match of html.matchAll(/\b(?:href|src)="([^"]+)"/g)) {
    const value = match[1];
    if (value.startsWith("#"))
      assert.ok(ids.includes(value.slice(1)), `missing anchor ${value}`);
    else if (!value.startsWith("https:"))
      assert.ok(existsSync(value), `missing file ${value}`);
  }
  for (const tag of html.matchAll(/<a\b[^>]*>/g)) {
    if (tag[0].includes("t.me/")) assert.ok(tag[0].includes("https://t.me/hacker_ronin"));
    if (tag[0].includes('target="_blank"'))
      assert.ok(tag[0].includes('rel="noopener noreferrer"'));
  }
  assert.ok(/<h1[^>]*>[^<]+/.test(html), "static hero content");
  assert.ok(html.includes('id="demo-open"') && (html.includes('id="lead-form"') || html.includes('id="lead-telegram"')));
  for (const key of ["canonical", "hreflang", "og:title", "og:description", "og:image"])
    assert.ok(html.includes(key));
  const config = JSON.parse(
    html.match(/<script type="application\/json" id="page-config">(.*?)<\/script>/s)[1],
  );
  assert.ok(config.error && config.calcNote && config.currency && config.variantA && config.variantB);
}
for (const [lang, file] of [
  ["ru", "index.html"],
  ["uz", "uz.html"],
  ["en", "en.html"],
])
  checkHTML(readFileSync(file, "utf8"), lang);
// Positive controls: the checker must catch a prohibited promise and missing local link.
const original = readFileSync("index.html", "utf8");
assert.throws(() => checkHTML(original + "<p>без комиссий</p>", "ru"));
assert.throws(() => checkHTML(original + '<a href="missing-file.html">x</a>', "ru"));
assert.throws(() =>
  checkHTML(original.replace("https://t.me/hacker_ronin", "https://t.me/wrong"), "ru"),
);
assert.ok(readFileSync("styles.css", "utf8").includes("prefers-reduced-motion"));
assert.ok(readFileSync("robots.txt", "utf8").includes("https://qadamup.uz/sitemap.xml"));
JSON.parse(readFileSync("site.webmanifest", "utf8"));
console.log("LANDING_STATIC_OK");
