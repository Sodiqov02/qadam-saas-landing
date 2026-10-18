/* All content lives in static HTML. JavaScript adds the calculator and mobile contact. */
(function () {
  "use strict";
  function calculateCosts(values) {
    const keys = ["orders", "average", "commission", "delivery", "other"];
    if (keys.some((key) => values[key] === "" || values[key] == null))
      return { state: "empty" };
    const numbers = keys.map((key) => Number(values[key]));
    if (numbers.some((n) => !Number.isFinite(n) || n < 0)) return { state: "invalid" };
    const [orders, average, rate, delivery, other] = numbers;
    if (
      !Number.isInteger(orders) ||
      orders > 1000000 ||
      average > 1e9 ||
      rate > 100 ||
      delivery > 1e9 ||
      other > 1e12
    )
      return { state: "invalid" };
    const turnover = orders * average;
    const commission = (turnover * rate) / 100;
    const deliveryTotal = orders * delivery;
    return {
      state: "valid",
      turnover,
      commission,
      delivery: deliveryTotal,
      other,
      total: commission + deliveryTotal + other,
    };
  }
  if (typeof module !== "undefined" && module.exports)
    module.exports = { calculateCosts };
  if (typeof document === "undefined") return;
  const config = JSON.parse(document.getElementById("page-config").textContent);
  const form = document.getElementById("cost-form");
  const status = document.getElementById("calculator-status");
  const formatter = new Intl.NumberFormat(config.locale, { maximumFractionDigits: 2 });
  function update() {
    const values = Object.fromEntries(
      ["orders", "average", "commission", "delivery", "other"].map((key) => [
        key,
        form.elements[key].value,
      ]),
    );
    const result = calculateCosts(values);
    if (
      Array.from(form.elements).some((input) => input.validity && input.validity.badInput)
    )
      result.state = "invalid";
    status.textContent =
      result.state === "invalid"
        ? config.calcError
        : result.state === "empty"
          ? config.calcEmpty
          : "";
    status.classList.toggle("error", result.state === "invalid");
    for (const key of ["turnover", "commission", "delivery", "other", "total"]) {
      document.getElementById("result-" + key).textContent =
        result.state === "valid"
          ? formatter.format(result[key]) + " " + config.currency
          : "—";
    }
  }
  form.addEventListener("input", update);
  form.addEventListener("submit", (event) => event.preventDefault());
  update();
  const mobileContact = document.querySelector(".mobile-contact");
  const hero = document.querySelector(".hero");
  const final = document.querySelector(".final-section");
  function updateContact() {
    const focusedInput =
      document.activeElement &&
      /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName);
    const show =
      hero.getBoundingClientRect().bottom < 0 &&
      final.getBoundingClientRect().top > innerHeight &&
      !focusedInput;
    mobileContact.classList.toggle("is-visible", show);
  }
  addEventListener("scroll", updateContact, { passive: true });
  addEventListener("resize", updateContact);
  document.addEventListener("focusin", updateContact);
  document.addEventListener("focusout", () => setTimeout(updateContact, 0));
  updateContact();
})();
