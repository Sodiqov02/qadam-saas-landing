# QadamUp final sales release

## Confirmed publication architecture

- Repository: `https://github.com/Sodiqov02/qadam-saas-landing`.
- Existing branch: `main`, root `/`, verified from live GitHub Pages configuration.
- Pages build type: legacy. GitHub runs its managed `pages-build-deployment` workflow; there is no custom repository workflow to replace.
- Domain: `qadamup.uz` in CNAME and Pages; HTTPS enforced with an approved certificate.
- Before release, local HEAD and origin/main were identical at `238d0ed680f35dab814185fa0dc29f254c804b31`. The working tree contained the earlier uncommitted landing and local server improvements. They are the authorized release foundation; no history rewrite or new branch is needed.
- RU is `/`, UZ `/uz.html`, EN `/en.html`, each a complete generated document with canonical, hreflang and Open Graph metadata.

## Final commercial changes

The retained Overdrive hero, scenario calculator and six-step demo remain. Telegram notification labels are now localized in RU/UZ/EN, with a clearer message bubble and synthetic customer data. Changing demo quantity updates the demo receipt and the separate Telegram example together. The backend notifier was read as source: it currently uses mixed English/Uzbek labels and fields for order/items/total/customer/contact/address/comment/source. The landing explicitly identifies its localized presentation as demonstration data; no backend translation or actual delivery is claimed. No Telegram status buttons were invented.

Fixed pricing explains predictable monthly service costs; percentage pricing explains fees related to actual order volume under agreed rules. No different feature entitlements were invented. Setup remains visibly 300,000 UZS, acquiring/delivery separate, with percentage charging rules and exchange rate agreed before payment. Duplicate pricing caveats were consolidated.

A compact proof block links to the working demo, transparent pricing, setup process and direct owner contact. There are no customer logos, invented testimonials, metrics or unsupported pilot claims.

## Production contact architecture

GitHub Pages cannot run `server.py` or SQLite. No deployed HTTPS lead API was established in the current infrastructure, so the authorized temporary Telegram option is used. The default `py -3 scripts/funnel.py` and compatible `scripts/build.py` generate Pages-safe HTML with a real contact anchor and localized draft text. The draft text is also readable/copyable on the page. Clicking opens Telegram; the visitor must send the message. No fake save or delivery success is shown, and contact works without JavaScript.

The public page explains that the automatic request form is currently local only. The retained local API mode is built with `py -3 scripts/funnel.py --target local`; server.py selects that mode at startup. Its existing protections and storage remain regression tested. Never commit local-mode HTML as the Pages release: `release_check.py` rejects it.

Telegram draft syntax uses the official public username link `https://t.me/<username>?text=<draft_text>` documented at [Telegram deep links](https://core.telegram.org/api/links#public-username-links). No bot token or automatic message sender is used. The configured owner link returned HTTP 200 in the release checks. This verifies availability of the contact page, not an actual message or response.

## Build and test

```powershell
py -3 scripts/funnel.py
py -3 scripts/release_regression.py
py -3 scripts/release_check.py
py -3 scripts/release_browser.py
```

The regression runner copies source to a temporary directory and builds local-mode HTML there; it does not turn production output back into a local API form. `build.py` still delegates to the current generator. Historical rendering cannot write stale HTML. `_config.yml` excludes scripts, local server, docs and artifacts from the Pages site.

`release_browser.py` uses a plain static HTTP server, with no lead API, and verifies three languages, old and new responsive widths, text contrast, calculator modes, two-item demo totals, FAQ keyboard behavior, assets, static contact destination, no-JS fallback and events without contact data. Telegram navigation is intercepted in tests; no message is sent. `--base https://qadamup.uz/` repeats the checks against production and compares returned HTML bytes with the release files.

Pre-publication acceptance passed: retained local regressions (including protected lead storage), current historical entry points, secret-pattern controls and static production browser checks. Static checks cover 27 responsive combinations (three languages × nine widths) plus three complete interaction groups. The retained local browser suite also covers its 18 responsive combinations. The final 4× CPU / 150 ms latency / 200 KB/s local lab recorded LCP 1164 ms and CLS 0, comparable to the previous local result; resource transfer rose from 93,980 to 95,721 bytes with the final trust/contact presentation. These are laboratory observations, not field Core Web Vitals.

Historical coverage and replaced requirements are mapped in [release-test-mapping.md](release-test-mapping.md). Current checks include negative controls for missing features, bad markup and recognized secret patterns. Pattern-based scanning supplements staged-file review; it is not a proof against every possible secret format.

## Video

No `.mp4`, `.mov` or `.webm` source footage was found in the checkout. The release does not fabricate footage and is not blocked on video. `docs/video.md` and `scripts/video.py` retain the future insertion/encoding path. Needed: approved readable menu→cart→checkout screen recording with synthetic data, an approved real Telegram receipt or clearly marked test recording, clean brand assets and approved audio; supply translations or review RU/UZ/EN subtitle text. A finished video or subtitles are not claimed.

## Release scope and remaining work

Only generated pages, required static assets, authoring/verification scripts, local lead server, relevant documentation, Pages exclusions and ignore rules belong in this commit. Local artifacts, SQLite, private configuration, caches and old acceptance ledgers stay out. The previous working state is recoverable from an external local archive; it is not published.

Remaining commercial operations: deployed secure lead API if an automatic form is wanted; bot setup and delivery validation for each restaurant; payment integration; agreed percentage-plan rules and billing exchange rate; operational contact handling and backups; real approved video/cases and field conversion/performance data. The local stdlib server is not presented as a production service. No conversion uplift or production readiness of payment/reservations/Mini App is claimed.
